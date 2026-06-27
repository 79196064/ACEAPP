from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database_models import get_db
from models.palline import Pallina

router = APIRouter(
    prefix="/tournament",
    tags=["ACEAI Tournament"]
)

class TournamentRequest(BaseModel):
    nome_utente: str
    superficie: str
    livello: str
    stile: str
    data_torneo: str
    ha_problemi_fisici: bool = False

@router.post("/prepara")
def prepara_torneo(dati: TournamentRequest, db: Session = Depends(get_db)):

    # Consigli superficie
    consigli_superficie = {
        "terra": {
            "racchetta": "Racchetta con pattern 16x19 per massimizzare lo spin",
            "corda": "Monofilamento poly sagomato per grip e spin",
            "tensione": "Tensione leggermente più bassa per più spin",
            "scarpe": "Scarpe con suola a spina di pesce per scivolata",
            "tattica": "Gioca lungo linea e usa il topspin pesante"
        },
        "cemento": {
            "racchetta": "Racchetta bilanciata con buon ammortizzamento",
            "corda": "Multifilamento o poly morbido per proteggere il braccio",
            "tensione": "Tensione media per controllo e potenza",
            "scarpe": "Scarpe con suola rinforzata per resistenza all abrasione",
            "tattica": "Gioco aggressivo da fondo con variazioni di ritmo"
        },
        "erba": {
            "racchetta": "Racchetta leggera e manovrabile per volée",
            "corda": "Budello naturale o multifilamento per massimo feel",
            "tensione": "Tensione più alta per controllo su superficie veloce",
            "scarpe": "Scarpe specifiche per erba con tacchetti",
            "tattica": "Serve and volley, gioco corto e variazioni"
        },
        "indoor": {
            "racchetta": "Racchetta versatile con buon controllo",
            "corda": "Multifilamento per feel e controllo",
            "tensione": "Tensione media alta per controllo su superficie rapida",
            "scarpe": "Scarpe indoor con suola non abrasiva",
            "tattica": "Gioco regolare con attenzione al rimbalzo basso"
        }
    }

    # Palline consigliate
    palline = db.query(Pallina).filter(
        Pallina.superficie == dati.superficie,
        Pallina.livello == dati.livello
    ).all()

    consiglio = consigli_superficie.get(dati.superficie, consigli_superficie["cemento"])

    # Warning fisici
    warning = []
    if dati.ha_problemi_fisici:
        warning.append("Attenzione: con problemi fisici scegli corde morbide e tensione bassa")
        warning.append("Considera un antivibro di qualita per ridurre le vibrazioni")

    return {
        "torneo": {
            "giocatore": dati.nome_utente,
            "superficie": dati.superficie,
            "data": dati.data_torneo,
            "livello": dati.livello
        },
        "setup_consigliato": consiglio,
        "palline_consigliate": [{"brand": p.brand, "modello": p.modello, "nota": p.nota} for p in palline],
        "warning": warning,
        "messaggio": f"Caro {dati.nome_utente}, ecco la tua preparazione ottimale per il torneo su {dati.superficie}!"
    }
