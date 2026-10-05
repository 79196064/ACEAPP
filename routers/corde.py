import re

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_models import get_db
from models.corde import Corda

from schemas import CordaSchema
from models.utenti import Utente
from routers.utenti import richiedi_ruolo

router = APIRouter(
    prefix="/corde",
    tags=["corde"]
)


def _calibro_mm(calibro: str | None) -> float | None:
    if not calibro:
        return None
    match = re.search(r"\d+(?:[.,]\d+)?", calibro)
    return float(match.group().replace(",", ".")) if match else None


def _classe_calibro(calibro_mm: float | None) -> str:
    if calibro_mm is None:
        return "non specificato"
    if calibro_mm <= 1.20:
        return "sottile"
    if calibro_mm <= 1.30:
        return "intermedio"
    return "spesso"

@router.get("/")
def get_corde(db: Session = Depends(get_db)):
    return db.query(Corda).all()


@router.get("/guida-tecnica")
def guida_tecnica_corde():
    """Soglie e definizioni tecniche estratte dalla scheda di riferimento."""
    return {
        "materiali": {
            "budello_naturale": "elasticita, tenuta di tensione e comfort elevati",
            "co_poly": "controllo e spin",
            "multifilo": "comfort e prestazioni simili al budello",
            "synthetic_gut": "soluzione bilanciata ed economica",
            "kevlar_aramide": "per ibridi ad alta resistenza",
        },
        "calibro_mm": {
            "sottile": "1.10-1.20 - spin e sensibilita, minore durata",
            "intermedio": "1.25-1.30 - equilibrio tra durata e prestazioni",
            "spesso": "> 1.35 - durata e controllo",
        },
        "forme": ["tonda", "sagomata (3-8 lati)", "rough", "twisted"],
        "tensione_kg": {"min": 18, "max": 28},
        "ibridi": {
            "classico": "monofilo sulle verticali, multi/budello sulle orizzontali",
            "reverse": "budello sulle verticali, monofilo sulle orizzontali",
        },
        "snapback": {
            "attrito_corda_corda_ottimale": "0.05-0.12",
            "attrito_corda_palla_ottimale": "0.40-0.60",
            "condizione": "la forza di richiamo deve superare l'attrito dinamico",
            "notching": "oltre circa 0.35 il movimento delle corde puo bloccarsi",
        },
        "coating": {
            "materiali": ["PTFE", "silicone", "fluoropolimeri"],
            "durata_co_poly_ore": "4-8 di gioco intenso",
        },
    }


@router.get("/{corda_id}/scheda-tecnica")
def scheda_tecnica_corda(corda_id: int, db: Session = Depends(get_db)):
    corda = db.query(Corda).filter(Corda.id == corda_id).first()
    if not corda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corda non trovata")

    calibro_mm = _calibro_mm(corda.calibro)
    return {
        "corda": {"id": corda.id, "brand": corda.brand, "modello": corda.model},
        "valori": {
            "materiale": corda.materiale,
            "calibro": corda.calibro,
            "forma_sezione": corda.forma_sezione,
            "texture": corda.texture,
            "rigidita_statica": corda.rigidita_statica,
            "rigidita_dinamica": corda.rigidita_dinamica,
            "perdita_tensione_percentuale": corda.perdita_tensione_percentuale,
            "resilienza": corda.resilienza,
            "resistenza_trazione": corda.resistenza_trazione,
            "attrito_corda_palla": corda.attrito_corda_palla,
            "attrito_corda_corda": corda.attrito_corda_corda,
            "snapback_score": corda.snapback_score,
            "tensione_min_kg": corda.tensione_min_kg,
            "tensione_max_kg": corda.tensione_max_kg,
            "coating": corda.coating,
            "durata_snapback_ore": corda.durata_snapback_ore,
            "compatibilita_ibrido": corda.compatibilita_ibrido,
        },
        "classificazione": {
            "calibro": _classe_calibro(calibro_mm),
            "snapback": "ottimale" if corda.attrito_corda_corda is not None and 0.05 <= corda.attrito_corda_corda <= 0.12 else "da valutare",
            "spin": "elevato" if corda.forma_sezione in {"sagomata", "rough", "twisted"} else "standard",
            "intervallo_tensione": (
                f"{corda.tensione_min_kg}-{corda.tensione_max_kg} kg"
                if corda.tensione_min_kg is not None and corda.tensione_max_kg is not None
                else "non specificato"
            ),
        },
    }


@router.post("/", response_model=CordaSchema, status_code=status.HTTP_201_CREATED)
def crea_corda(
    dati: CordaSchema,
    db: Session = Depends(get_db),
    _: Utente = Depends(richiedi_ruolo("admin")),
):
    esistente = db.query(Corda).filter(
        Corda.brand == dati.brand,
        Corda.model == dati.model,
    ).first()
    if esistente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Corda gia presente")
    corda = Corda(**dati.model_dump(exclude={"id"}))
    db.add(corda)
    db.commit()
    db.refresh(corda)
    return corda


@router.put("/{corda_id}", response_model=CordaSchema)
def aggiorna_corda(
    corda_id: int,
    dati: CordaSchema,
    db: Session = Depends(get_db),
    _: Utente = Depends(richiedi_ruolo("admin")),
):
    corda = db.query(Corda).filter(Corda.id == corda_id).first()
    if not corda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corda non trovata")
    for campo, valore in dati.model_dump(exclude={"id"}).items():
        setattr(corda, campo, valore)
    db.commit()
    db.refresh(corda)
    return corda
