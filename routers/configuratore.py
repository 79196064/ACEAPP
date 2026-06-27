import os
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import dei modelli dal tuo modulo database
from database_models import get_db
from models.racchette import Racchetta
from models.corde import Corda
from models.antivibro import Antivibro

# Import dei servizi dell'algoritmo e dell'IA di ACEAI
from services.aceai import (
    PlayerProfile,
    Racquet,
    StringItem,
    score_racquet_for_player,
    score_string_for_player,
    calculate_tension,
    generate_ai_explanation
)

from pydantic import BaseModel

# Inizializzazione Router
router = APIRouter(
    prefix="/configuratore",
    tags=["Configuratore Visivo"]
)

# ─────────────────────────────────────────
# SCHEMI SCHEMI DI RICHIESTA (PYDANTIC)
# ─────────────────────────────────────────

class ConfigurazioneRequest(BaseModel):
    racchetta_brand: str
    racchetta_modello: str
    corda_brand: str
    corda_modello: str
    colore_grip: str = "nero"
    colore_corda: str = "naturale"
    antivibro: str = "nessuno"
    livello: str = "intermedio"  # "beginner", "intermediate", "advanced"
    stile: str = "difensore"     # "attaccante", "arrotino", "difensore"

    # Aggiornamento Pydantic V2 per evitare i warning nel terminale
    model_config = {
        "from_attributes": True
    }


# ─────────────────────────────────────────
# ENDPOINT GET: RACCHETTE
# ─────────────────────────────────────────

@router.get("/racchette")
def get_racchette_configuratore(db: Session = Depends(get_db)):
    racchette = db.query(Racchetta).all()
    return [
        {
            "id": r.id,
            "brand": r.brand,
            "modello": r.model,
            "immagine": getattr(r, "image_url", None),
            "colori_disponibili": ["nero", "bianco", "rosso", "blu", "giallo"]
        }
        for r in racchette
    ]


# ─────────────────────────────────────────
# ENDPOINT GET: CORDE
# ─────────────────────────────────────────

@router.get("/corde")
def get_corde_configuratore(db: Session = Depends(get_db)):
    corde = db.query(Corda).all()
    return [
        {
            "id": c.id,
            "brand": c.brand,
            "modello": c.model,
            "materiale": getattr(c, "materiale", "poly"),
            "colori_disponibili": ["naturale", "nero", "rosso", "blu", "giallo", "arancione"]
        }
        for c in corde
    ]


# ─────────────────────────────────────────
# ENDPOINT POST: GENERA CONFIGURAZIONE (INTEGRAZIONE IA)
# ─────────────────────────────────────────

@router.post("/genera")
def genera_configurazione(dati: ConfigurazioneRequest, db: Session = Depends(get_db)):
    # 1. Cerca l'attrezzatura reale nel database per estrarre le specifiche fisiche
    racchetta_db = db.query(Racchetta).filter(
        Racchetta.brand == dati.racchetta_brand,
        Racchetta.model == dati.racchetta_modello
    ).first()

    corda_db = db.query(Corda).filter(
        Corda.brand == dati.corda_brand,
        Corda.model == dati.corda_modello
    ).first()

    # Fallback se i dati inseriti non sono ancora nel database
    if not racchetta_db:
        # Crea specifiche fittizie di sicurezza per non bloccare l'esecuzione
        info_racchetta = Racquet(dati.racchetta_brand, dati.racchetta_modello, 64, "16x19", 23.0, 300)
    else:
        info_racchetta = Racquet(
            brand=racchetta_db.brand,
            model=racchetta_db.model,
            stiffness_ra=getattr(racchetta_db, "stiffness_ra", 64),
            pattern=getattr(racchetta_db, "pattern", "16x19"),
            profile_mm=getattr(racchetta_db, "profile_mm", 23.0),
            weight_g=getattr(racchetta_db, "weight_g", 300)
        )

    if not corda_db:
        info_corda = StringItem(dati.corda_modello, "poly", True, 60)
    else:
        info_corda = StringItem(
            name=corda_db.model,
            material=getattr(corda_db, "materiale", "poly"),
            is_shaped=(getattr(corda_db, "materiale", "poly") == "poly"),
            stiffness_score=60
        )

    # 2. Istanzia il profilo del giocatore
    # Converte le stringhe del frontend nei formati previsti dall'algoritmo
    livello_mappa = {"principiante": "beginner", "intermedio": "intermediate", "avanzato": "advanced"}
    livello_tecnico = livello_mappa.get(dati.livello.lower(), dati.livello)

    profilo = PlayerProfile(
        level=livello_tecnico,
        style=dati.stile.lower(),
        prefers_spin=(dati.stile.lower() == "arrotino"),
        prefers_power=(dati.stile.lower() == "attaccante"),
        prefers_control=(dati.stile.lower() == "difensore")
    )

    # 3. Calcolo degli Score e delle tensioni con aceai.py
    racquet_score = score_racquet_for_player(profilo, info_racchetta)
    string_score = score_string_for_player(profilo, info_corda)
    tensioni = calculate_tension(profilo)
    
    # Calcolo del punteggio base unito alle logiche del tuo backend originale
    score_base = (racquet_score + string_score) / 2
    if dati.livello == "avanzato":
        score_base += 15
    elif dati.livello == "intermedio":
        score_base += 8

    if dati.stile == "arrotino" and dati.colore_corda != "naturale":
        score_base += 5
    if dati.antivibro != "nessuno":
        score_base += 5

    score_finale = max(0.0, min(100.0, score_base))

    # 4. Generazione dei consigli visivi statici
    consigli_visivi = []
    if dati.colore_grip == "bianco":
        consigli_visivi.append("Il grip bianco si sporca facilmente - considera il nero se giochi molto frequentemente.")
    if dati.colore_corda == "naturale":
        consigli_visivi.append("La corda naturale offre feel superiore ma perde tensione più rapidamente rispetto ai polimeri.")

    # 5. Generazione spiegazione tecnica personalizzata con Claude AI
    combo_dati_ia = {
        "racquet_brand": info_racchetta.brand,
        "racquet_model": info_racchetta.model,
        "racquet_score": racquet_score,
        "string_name": info_corda.name,
        "string_score": string_score,
        "tension_main": tensioni["tension_main"],
        "tension_cross": tensioni["tension_cross"],
        "total_score": score_finale,
        "reason_template": f"Setup calibrato ottimamente per un gioco da {dati.stile}."
    }
    spiegazione_ia = generate_ai_explanation(profilo, combo_dati_ia)

    # 6. Risposta strutturata finale per l'applicazione
    return {
        "configurazione": {
            "racchetta": {
                "brand": dati.racchetta_brand,
                "modello": dati.racchetta_modello,
                "colore_grip": dati.colore_grip,
            },
            "corda": {
                "brand": dati.corda_brand,
                "modello": dati.corda_modello,
                "colore": dati.colore_corda,
            },
            "antivibro": dati.antivibro,
        },
        "score_configurazione": score_finale,
        "consigli_visivi": consigli_visivi,
        "pronto_per_3d": True,
        "pronto_per_ar": True,
        "messaggio": f"La tua configurazione {dati.racchetta_brand} {dati.racchetta_modello} è pronta per il campo.",
        "prossimo_step": "Aggiungi al carrello o verifica disponibilità nei negozi partner.",
        "tensioni_consigliate": tensioni,
        "recensione_tecnica_ia": spiegazione_ia
    }


# ─────────────────────────────────────────
# ENDPOINT GET: COLORI DISPONIBILI
# ─────────────────────────────────────────

@router.get("/colori-disponibili")
def get_colori_disponibili():
    return {
        "grip": ["nero", "bianco", "rosso", "blu", "giallo", "verde", "arancio"],
        "corda": ["naturale", "nero", "rosso", "blu", "giallo", "arancio", "verde"],
        "antivibro": ["nessuno", "rotondo", "a_w", "lungo", "custom"]
    }
