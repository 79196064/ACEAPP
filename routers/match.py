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
from models.scarpe import Scarpa  # 🟢 Importo il tuo modello delle scarpe esistente
from services.aceai import (
    genera_consulenza, PlayerProfile, Racquet, StringItem, BallItem, ShoeItem
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/match", tags=["ACEAI Match"])

# Modello dati allineato al 100% con il Frontend di Lovable.dev
class MatchRequest(BaseModel):
    nome: str
    livello: str
    stile: str
    superficie: str
    problema_fisico: str  
    # Campi biometrici estratti dalle schermate
    eta: Optional[int] = None              
    peso: Optional[int] = None             
    altezza: Optional[int] = None          
    genere: Optional[str] = None           
    sesso: Optional[str] = None            
    citta: Optional[str] = None            
    taglia_tshirt: Optional[str] = None    
    taglia_pantaloncini: Optional[str] = None
    numero_scarpe: Optional[int] = None    
    colore_preferito: Optional[str] = None 
    # Obiettivo ed email
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
    # 1. Lettura tabelle dal Database (Aggiunta la query per le scarpe)
    racchette_db = db.query(Racchetta).all()
    corde_db = db.query(Corda).all()
    palline_db = db.query(Pallina).all()
    scarpe_db = db.query(Scarpa).all()  # 🟢 Estrazione dei dati reali delle scarpe

    # 2. Conversione Database → Oggetti logici ACEAI
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

    # 🟢 Mappatura delle scarpe per l'algoritmo
    shoes = [
        ShoeItem(
            brand=getattr(s, 'brand', 'Asics'),
            modello=getattr(s, 'modello', 'Gel-Resolution'),
            superficie=getattr(s, 'superficie', 'all court'),
            livello=getattr(s, 'livello', 'intermedio'),
            nota=getattr(s, 'nota', getattr(s, 'note', '')) or ''
        ) for s in scarpe_db
    ]

    # 3. Normalizzazione difensiva delle risposte
    problema = dati.problema_fisico.lower() if dati.problema_fisico else ""
    obiettivo = dati.obiettivo.lower() if dati.obiettivo else ""

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
        prefers_control=("controllo" in obiettivo),
        preferred_color=dati.colore_preferito,
        # Assegnazione dei parametri biologici reali
        age=dati.eta,
        weight=dati.peso,
        height=dati.altezza,
        gender=dati.genere.lower() if dati.genere else None,
        numero_scarpe=dati.numero_scarpe
    )

    # 4. Generazione consulenza estesa (ora passiamo anche la lista delle scarpe!)
    risposta = genera_consulenza(player, racquets, strings, balls, shoes)
    risposta["messaggio"] = f"Ciao {dati.nome}! Ecco la tua consulenza personalizzata."
    
    # 5. Spedizione mail in background
    if dati.email and dati.email.strip():
        background_tasks.add_task(esegui_invio_email, dati.nome, dati.email, risposta)

    return risposta
