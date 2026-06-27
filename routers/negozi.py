from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database_models import get_db
from models.negozi import Negozio

router = APIRouter(
    prefix="/negozi",
    tags=["Negozi"]
)

class NegozioCreate(BaseModel):
    nome: str
    citta: str
    indirizzo: Optional[str] = None
    telefono: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    sito_web: Optional[str] = None
    logo_url: Optional[str] = None
    foto_negozio_url: Optional[str] = None
    superficie_campi: Optional[str] = None
    servizi: Optional[str] = None
    fascia_prezzi: Optional[str] = None
    latitudine: Optional[float] = None
    longitudine: Optional[float] = None
    regione: Optional[str] = None
    banner_url: Optional[str] = None

@router.get("/")
def get_negozi(db: Session = Depends(get_db)):
    return db.query(Negozio).filter(Negozio.attivo == True).all()

@router.get("/citta/{citta}")
def get_negozi_by_citta(citta: str, db: Session = Depends(get_db)):
    return db.query(Negozio).filter(Negozio.citta == citta, Negozio.attivo == True).all()

@router.get("/{negozio_id}")
def get_negozio(negozio_id: int, db: Session = Depends(get_db)):
    return db.query(Negozio).filter(Negozio.id == negozio_id).first()

@router.post("/")
def crea_negozio(dati: NegozioCreate, db: Session = Depends(get_db)):
    negozio = Negozio(
        nome=dati.nome,
        citta=dati.citta,
        indirizzo=dati.indirizzo,
        telefono=dati.telefono,
        whatsapp=dati.whatsapp,
        email=dati.email,
        sito_web=dati.sito_web,
        logo_url=dati.logo_url,
        foto_negozio_url=dati.foto_negozio_url,
        superficie_campi=dati.superficie_campi,
        servizi=dati.servizi,
        fascia_prezzi=dati.fascia_prezzi,
        attivo=True
    )
    db.add(negozio)
    db.commit()
    db.refresh(negozio)
    return {"status": "ok", "id": negozio.id, "messaggio": f"Negozio {dati.nome} inserito con successo!"}
