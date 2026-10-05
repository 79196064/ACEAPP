from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database_models import get_db
from models.racchette import Racchetta
from models.corde import Corda

router = APIRouter(
    prefix="/comparison",
    tags=["ACEAI Comparison"]
)

class ComparisonRequest(BaseModel):
    racchetta_attuale_brand: str
    racchetta_attuale_modello: str
    racchetta_consigliata_brand: str
    racchetta_consigliata_modello: str
    livello: str
    stile: str

@router.post("/racchette")
def confronta_racchette(dati: ComparisonRequest):
    score_attuale = 50
    score_consigliata = 75

    if dati.livello == "principiante":
        score_attuale -= 5
        score_consigliata += 10
    elif dati.livello == "avanzato":
        score_consigliata += 15

    if dati.stile == "arrotino":
        score_consigliata += 10
    elif dati.stile == "attaccante":
        score_consigliata += 8

    differenza = score_consigliata - score_attuale

    return {
        "racchetta_attuale": {
            "brand": dati.racchetta_attuale_brand,
            "modello": dati.racchetta_attuale_modello,
            "score": score_attuale,
        },
        "racchetta_consigliata": {
            "brand": dati.racchetta_consigliata_brand,
            "modello": dati.racchetta_consigliata_modello,
            "score": score_consigliata,
        },
        "differenza_score": differenza,
        "miglioramento": f"+{differenza} punti di performance",
        "vale_la_pena_cambiare": differenza >= 15,
        "messaggio": f"Passando a {dati.racchetta_consigliata_brand} {dati.racchetta_consigliata_modello} potresti migliorare le tue prestazioni di {differenza} punti!"
    }
