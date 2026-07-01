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

# 🟢 Modello aggiornato con tutti i dati biometrici e le selezioni del Frontend di Lovable
class MatchRequest(BaseModel):
    nome: str
    livello: str
    stile: str
    superficie: str
    problema_fisico: str  # Gestisce la selezione sul braccio/epicondilite
    obiettivo: str
    email: str = ""
    
    # Nuovi campi inseriti nelle schermate 1, 2 e 3
    genere: Optional[str] = None           # Uomo / Donna / Bambino
    sesso: Optional[str] = None            # Maschio / Femmina
    altezza: Optional[int] = None          # es. 175
    peso: Optional[int] = None             # es. 70
    eta: Optional[int] = None              # es. 30
    citta: Optional[str] = None            
    taglia_tshirt: Optional[str] = None    
    taglia_pantaloncini: Optional[str] = None
    numero_scarpe: Optional[int] = None    
    colore_preferito: Optional[str] = None 
    
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
    # 1. Lettura tabelle DB
    racchette_db = db.query(Racchetta).all()
    corde_db = db.query(Corda).all()
    palline_db = db.query(Pallina).all()

    # 2. Conversione DB → ACEAI
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

    # 3. Normalizzazione difensiva delle risposte (Evita bug se cambiano le maiuscole)
    problema = dati.problema_fisico.lower() if dati.problema_fisico else ""
    obiettivo = dati.obiettivo.lower() if dati.obiettivo else ""

    # Controllo intelligente per l'epicondilite/problema braccio
    ha_problemi_gomito = (
        "gomito" in problema or 
        "si" in problema or 
        "epicondilite" in problema or 
        "occasionalmente" in problema
    )

    player = PlayerProfile(
        level=dati.livello.lower() if dati.livello else "intermedio",
        style=dati.stile.lower() if dati.stile else "tutto campo",
        surface=dati.superficie.lower() if dati.superficie else "terra",
        has_elbow_issues=ha_problemi_gomito,
        has_shoulder_issues=("spalla" in problema),
        has_wrist_issues=("polso" in problema),
        prefers_spin=("spin" in obiettivo),
        prefers_power=("potenza" in obiettivo),
        prefers_control=("controllo" in obiettivo)
    )

    # 4. Generazione consulenza
    risposta = genera_consulenza(player, racquets, strings, balls)
    risposta["messaggio"] = f"Ciao {dati.nome}! Ecco la tua consulenza personalizzata."
    
    # 5. Spedizione mail in background
    if dati.email and dati.email.strip():
        background_tasks.add_task(esegui_invio_email, dati.nome, dati.email, risposta)

    return risposta
