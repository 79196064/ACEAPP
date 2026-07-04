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
    altezza: int = 0
    peso: int = 0
    eta: int = 0
    genere: str = ""
    model_config = {"from_attributes": True}
def categorizza_corda(brand, modello):
    testo = f"{brand} {modello}".lower()
    if any(x in testo for x in ["rpm", "hurricane", "spin", "rough", "revolution"]):
        return {"material": "poly", "is_shaped": True, "stiffness_score": 75}
    elif any(x in testo for x in ["gut", "natural", "vs team"]):
        return {"material": "gut", "is_shaped": False, "stiffness_score": 35}
    elif any(x in testo for x in ["multi", "biophonix", "nrg", "xcel"]):
        return {"material": "multi", "is_shaped": False, "stiffness_score": 45}
    elif any(x in testo for x in ["synthetic", "nylon", "prince"]):
        return {"material": "synthetic gut", "is_shaped": False, "stiffness_score": 50}
    else:
        return {"material": "poly", "is_shaped": False, "stiffness_score": 60}

def categorizza_racchetta(brand, modello):
    testo = f"{brand} {modello}".lower()
    if any(x in testo for x in ["pro staff", "prestige", "phantom", "speed pro"]):
        return {"stiffness_ra": 62, "pattern": "18x20", "profile_mm": 21.0, "weight_g": 315}
    elif any(x in testo for x in ["pure aero", "gravity", "extreme"]):
        return {"stiffness_ra": 68, "pattern": "16x19", "profile_mm": 24.0, "weight_g": 300}
    elif any(x in testo for x in ["clash", "instinct", "radical"]):
        return {"stiffness_ra": 58, "pattern": "16x19", "profile_mm": 26.0, "weight_g": 285}
    elif any(x in testo for x in ["junior", "team", "boost", "recreational"]):
        return {"stiffness_ra": 72, "pattern": "16x19", "profile_mm": 25.0, "weight_g": 270}
    else:
        return {"stiffness_ra": 65, "pattern": "16x19", "profile_mm": 23.0, "weight_g": 300}


@router.post("/consulenza")
def consulenza_match(dati: MatchRequest):
    from models.racchette import Racchetta
    from models.corde import Corda
    from models.palline import Pallina
    from database_models import SessionLocal

    db = SessionLocal()
    racchette_db = db.query(Racchetta).all()
    corde_db = db.query(Corda).all()
    palline_db = db.query(Pallina).all()
    db.close()

    racquets = [
        Racquet(
            brand=r.brand,
            model=r.modello,
            **categorizza_racchetta(r.brand, r.modello)
        ) for r in racchette_db
    ]

        strings = [
        StringItem(
            name=f"{c.brand} {c.model}" if hasattr(c, 'model') else str(c.brand),
            **categorizza_corda(c.brand, getattr(c, 'model', ''))
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

     player = PlayerProfile(
        level=dati.livello.lower(),
        style=dati.stile.lower(),
        surface=dati.superficie.lower(),
        has_elbow_issues=(dati.problema_fisico.lower() == "gomito"),
        has_shoulder_issues=(dati.problema_fisico.lower() == "spalla"),
        has_wrist_issues=(dati.problema_fisico.lower() == "polso"),
        prefers_spin=(dati.obiettivo.lower() == "spin"),
        prefers_power=(dati.obiettivo.lower() == "potenza"),
        prefers_control=(dati.obiettivo.lower() == "controllo"),
        age=dati.eta if dati.eta > 0 else None,
        weight=dati.peso if dati.peso > 0 else None,
        height=dati.altezza if dati.altezza > 0 else None,
        gender=dati.genere.lower() if dati.genere else None
    )   

    risposta = genera_consulenza(player, racquets, strings, balls)
    risposta["messaggio"] = f"Ciao {dati.nome}! Ecco la tua consulenza personalizzata."

    try:
        from services.email import invia_email_consulenza
        if dati.email:
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