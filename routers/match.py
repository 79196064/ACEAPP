import os
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database_models import SessionLocal
from models.racchette import Racchetta
from models.corde import Corda
from models.palline import Pallina
from services.aceai import (
    genera_consulenza, PlayerProfile, Racquet, StringItem, BallItem
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/match", tags=["ACEAI Match"])

class MatchRequest(BaseModel):
    nome: str
    livello: str
    stile: str
    superficie: str
    problema_fisico: str
    obiettivo: str
    email: str = ""
    
    model_config = {"from_attributes": True}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def esegui_invio_email(dati_nome: str, dati_email: str, risposta: dict):
    try:
        from services.email import invia_email_consulenza
        invia_email_consulenza(
            nome=dati_nome,
            email=dati_email,
            setup=risposta.get("setup", {}),
            score=risposta.get("profilo", {}).get("score_profilo", 0),
            spiegazione=risposta.get("spiegazione_aceai", "")
        )
    except Exception as e:
        logger.error(f"Errore invio email consulenza: {str(e)}")

@router.post("/consulenza")
async def consulenza_match(
    dati: MatchRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    racchette_db = db.query(Racchetta).all()
    corde_db = db.query(Corda).all()
    palline_db = db.query(Pallina).all()

    racquets = [
        Racquet(
            brand=getattr(r, 'brand', 'Generic'),
            model=getattr(r, 'modello', 'Generic'),
            stiffness_ra=getattr(r, 'stiffness_ra', 65) or 65,
            pattern=getattr(r, 'pattern', '16x19') or '16x19',
            profile_mm=getattr(r, 'profile_mm', 23.0) or 23.0,
            weight_g=getattr(r, 'weight_g', getattr(r, 'peso', 300)) or 300
        ) for r in racchette_db
    ]

    strings = [
        StringItem(
            name=f"{c.brand} {getattr(c, 'model', getattr(c, 'modello', ''))}".strip() if hasattr(c, 'brand') else "Generic",
            material=getattr(c, 'materiale', 'poly') or 'poly',
            is_shaped=getattr(c, 'is_shaped', getattr(c, 'sagomata', False)) or False,
            stiffness_score=getattr(c, 'stiffness_score', getattr(c, 'rigidezza', 60)) or 60
        ) for c in corde_db
    ]

    balls = [
        BallItem(
            brand=getattr(b, 'brand', 'Wilson'),
            modello=getattr(b, 'modello', 'US Open'),
            superficie=getattr(b, 'superficie', 'terra'),
            livello=getattr(b, 'livello', 'intermedio'),
            nota=getattr(b, 'note', getattr(b, 'nota', '')) or ''
        ) for b in palline_db
    ]

    problema = dati.problema_fisico.lower()
    obiettivo = dati.obiettivo.lower()

    player = PlayerProfile(
        level=dati.livello.lower(),
        style=dati.stile.lower(),
        surface=dati.superficie.lower(),
        has_elbow_issues=(problema == "gomito"),
        has_shoulder_issues=(problema == "spalla"),
        has_wrist_issues=(problema == "polso"),
        prefers_spin=(obiettivo == "spin"),
        prefers_power=(obiettivo == "potenza"),
        prefers_control=(obiettivo == "controllo")
    )

    risposta = genera_consulenza(player, racquets, strings, balls)
    risposta["messaggio"] = f"Ciao {dati.nome}! Ecco la tua consulenza personalizzata."
    
    if dati.email and dati.email.strip():
        background_tasks.add_task(esegui_invio_email, dati.nome, dati.email, risposta)

    return risposta
 