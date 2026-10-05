from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_models import get_db

from models.racchette import Racchetta

from schemas import RacchettaSchema
from models.utenti import Utente
from routers.utenti import richiedi_ruolo

router = APIRouter(
    prefix="/racchette",
    tags=["racchette"]
)


def _profilo_medio_mm(profilo: str | None) -> float | None:
    if not profilo:
        return None
    try:
        valori = [float(valore) for valore in profilo.replace("mm", "").split("-")]
        return sum(valori) / len(valori)
    except ValueError:
        return None


def _classe_intervallo(valore, soglie, etichette):
    if valore is None:
        return "non specificato"
    for soglia, etichetta in zip(soglie, etichette):
        if valore < soglia:
            return etichetta
    return etichette[-1]

@router.get("/")
def get_racchette(db: Session = Depends(get_db)):
    return db.query(Racchetta).all()


@router.get("/guida-tecnica")
def guida_tecnica_racchette():
    """Soglie e definizioni tecniche estratte dalla scheda di riferimento."""
    return {
        "lunghezza_cm": {"standard": 68.5, "extended_max": 71.0},
        "head_size_in2": {
            "midsize": "< 95",
            "midplus": "95-105",
            "oversize": "> 105",
        },
        "profilo_mm": {
            "sottile": "17-22 (controllo e flessione)",
            "largo": "23-28 (potenza e rigidita)",
        },
        "grip": {"L1": 105, "L2": 108, "L3": 111, "L4": 114, "L5": 118},
        "peso_non_incordata_g": {
            "leggera": "255-280",
            "intermedia": "285-300",
            "tour": "305-340",
        },
        "bilanciamento_cm": {
            "al_manico": "< 32",
            "neutro": "32-33",
            "in_testa": "> 33",
        },
        "swingweight": {"basso": "< 300", "alto": "> 325"},
        "rigidita_ra": {
            "flessibile": "< 63",
            "media": "63-67",
            "rigida": "> 67",
        },
        "pattern_corde": {
            "aperto": "16x19 - spin e potenza",
            "denso": "18x20 - controllo e precisione",
        },
        "materiali_comuni": [
            "grafite ad alto modulo",
            "kevlar/aramide",
            "carbonio intrecciato",
            "grafene",
            "resine epossidiche",
            "poliuretano espanso nel manico",
        ],
        "componenti": ["grommets", "grip di base", "butt cap", "sezione manico ottagonale"],
    }


@router.get("/{racchetta_id}/scheda-tecnica")
def scheda_tecnica_racchetta(racchetta_id: int, db: Session = Depends(get_db)):
    racchetta = db.query(Racchetta).filter(Racchetta.id == racchetta_id).first()
    if not racchetta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Racchetta non trovata")

    bilanciamento_cm = (
        racchetta.bilanciamento / 10 if racchetta.bilanciamento and racchetta.bilanciamento > 100
        else racchetta.bilanciamento
    )
    profilo_medio = _profilo_medio_mm(racchetta.profilo)
    return {
        "racchetta": {"id": racchetta.id, "brand": racchetta.brand, "modello": racchetta.modello},
        "valori": {
            "head_size_in2": racchetta.piatto_corde,
            "peso_non_incordata_g": racchetta.peso,
            "peso_incordata_g": racchetta.peso_incordata,
            "bilanciamento_cm": bilanciamento_cm,
            "schema_corde": racchetta.schema_corde,
            "profilo_mm": racchetta.profilo,
            "profilo_medio_mm": profilo_medio,
            "rigidita_ra": racchetta.rigidita,
            "swingweight": racchetta.swingweight,
            "lunghezza_cm": racchetta.lunghezza_cm,
            "punti_head_light": racchetta.punti_head_light,
            "grip_disponibili": racchetta.grip_disponibili,
            "materiali": racchetta.materiali,
            "grommets": racchetta.grommets,
            "tipo_fori": racchetta.tipo_fori,
        },
        "classificazione": {
            "head_size": _classe_intervallo(racchetta.piatto_corde, [95, 106], ["midsize", "midplus", "oversize"]),
            "peso": _classe_intervallo(racchetta.peso, [285, 305], ["leggera", "intermedia", "tour"]),
            "bilanciamento": _classe_intervallo(bilanciamento_cm, [32, 33], ["al manico", "neutro", "in testa"]),
            "profilo": _classe_intervallo(profilo_medio, [23, 29], ["sottile", "largo", "extra largo"]),
            "rigidita": _classe_intervallo(racchetta.rigidita, [63, 68], ["flessibile", "media", "rigida"]),
            "swingweight": _classe_intervallo(racchetta.swingweight, [300, 326], ["basso", "medio", "alto"]),
        },
    }


@router.post("/", response_model=RacchettaSchema, status_code=status.HTTP_201_CREATED)
def crea_racchetta(
    dati: RacchettaSchema,
    db: Session = Depends(get_db),
    _: Utente = Depends(richiedi_ruolo("admin")),
):
    esistente = db.query(Racchetta).filter(
        Racchetta.brand == dati.brand,
        Racchetta.modello == dati.modello,
    ).first()
    if esistente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Racchetta gia presente")
    racchetta = Racchetta(**dati.model_dump(exclude={"id"}))
    db.add(racchetta)
    db.commit()
    db.refresh(racchetta)
    return racchetta


@router.put("/{racchetta_id}", response_model=RacchettaSchema)
def aggiorna_racchetta(
    racchetta_id: int,
    dati: RacchettaSchema,
    db: Session = Depends(get_db),
    _: Utente = Depends(richiedi_ruolo("admin")),
):
    racchetta = db.query(Racchetta).filter(Racchetta.id == racchetta_id).first()
    if not racchetta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Racchetta non trovata")
    for campo, valore in dati.model_dump(exclude={"id"}).items():
        setattr(racchetta, campo, valore)
    db.commit()
    db.refresh(racchetta)
    return racchetta
