import os
from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from services.aceai import genera_consulenza, PlayerProfile
from services.aceai import Racquet, StringItem, BallItem


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

@router.post("/consulenza")
def consulenza_match(dati: MatchRequest):
    from models.racchette import Racchetta
    from models.corde import Corda
    from models.palline import Pallina
    from database_models import SessionLocal


    db = SessionLocal()

    # 🔥 Lettura dati reali dal DB
    racchette_db = db.query(Racchetta).all()
    corde_db = db.query(Corda).all()
    palline_db = db.query(Pallina).all()
    db.close()

    # 🔥 Conversione DB → ACEAI
    racquets = [
        Racquet(
            brand=r.brand,
            model=r.modello,
            stiffness_ra=65,
            pattern="16x19",
            profile_mm=23.0,
            weight_g=300
        ) for r in racchette_db
    ]

    strings = [
        StringItem(
            name=f"{c.brand} {c.model}" if hasattr(c, 'model') else str(c.brand),
            material=getattr(c, 'materiale', 'poly') or 'poly',
            is_shaped=False,
            stiffness_score=60
        ) for c in corde_db
    ]

    balls = [
        BallItem(
            brand=getattr(b, 'brand', 'Wilson'),
            modello=getattr(b, 'modello', 'US Open'),
            superficie=getattr(b, 'superficie', 'terra'),
            livello=getattr(b, 'livello', 'intermedio'),
            nota=getattr(b, 'note', '') or ''
        ) for b in palline_db
    ]

    # 🔥 Profilo giocatore
    player = PlayerProfile(
        level=dati.livello.lower(),
        style=dati.stile.lower(),
        surface=dati.superficie.lower(),
        has_elbow_issues=(dati.problema_fisico.lower() == "gomito"),
        has_shoulder_issues=(dati.problema_fisico.lower() == "spalla"),
        has_wrist_issues=(dati.problema_fisico.lower() == "polso"),
        prefers_spin=(dati.obiettivo.lower() == "spin"),
        prefers_power=(dati.obiettivo.lower() == "potenza"),
        prefers_control=(dati.obiettivo.lower() == "controllo")
    )

    risposta = genera_consulenza(player, racquets, strings, balls)
    risposta["messaggio"] = f"Ciao {dati.nome}! Ecco la tua consulenza personalizzata."
    try:
        from services.email import invia_email_consulenza
        if hasattr(dati, 'email') and dati.email:
            invia_email_consulenza(
                nome=dati.nome,
                email=dati.email,
                setup=risposta.get("setup", {}),
                score=risposta.get("profilo", {}).get("score_profilo", 0),
                spiegazione=risposta.get("spiegazione_aceai", "")
            )
    except Exception as e:
        print(f"Errore invio email consulenza: {str(e)}")
    return risposta
    