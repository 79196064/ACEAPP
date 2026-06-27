from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel
from database_models import get_db, Base
from datetime import datetime

class Evolution(Base):
    __tablename__ = "evolution"
    id = Column(Integer, primary_key=True, index=True)
    nome_utente = Column(String, nullable=False)
    data = Column(String, nullable=False)
    livello = Column(String, nullable=False)
    racchetta = Column(String, nullable=False)
    corda = Column(String, nullable=False)
    tensione_main = Column(Integer, nullable=False)
    tensione_cross = Column(Integer, nullable=False)
    superficie = Column(String, nullable=False)
    note = Column(String, nullable=True)

router = APIRouter(
    prefix="/evolution",
    tags=["ACEAI Evolution"]
)

class EvolutionRequest(BaseModel):
    nome_utente: str
    livello: str
    racchetta: str
    corda: str
    tensione_main: int
    tensione_cross: int
    superficie: str
    note: str = ""

@router.post("/salva")
def salva_setup(dati: EvolutionRequest, db: Session = Depends(get_db)):
    entry = Evolution(
        nome_utente=dati.nome_utente,
        data=datetime.now().strftime("%Y-%m-%d %H:%M"),
        livello=dati.livello,
        racchetta=dati.racchetta,
        corda=dati.corda,
        tensione_main=dati.tensione_main,
        tensione_cross=dati.tensione_cross,
        superficie=dati.superficie,
        note=dati.note
    )
    db.add(entry)
    db.commit()
    return {"status": "salvato", "messaggio": f"Setup di {dati.nome_utente} salvato con successo!"}

@router.get("/storico/{nome_utente}")
def storico_utente(nome_utente: str, db: Session = Depends(get_db)):
    storico = db.query(Evolution).filter(Evolution.nome_utente == nome_utente).all()
    if not storico:
        return {"messaggio": f"Nessuno storico trovato per {nome_utente}"}

    primo = storico[0]
    ultimo = storico[-1]

    evoluzione = []
    if len(storico) > 1:
        if ultimo.tensione_main > primo.tensione_main:
            evoluzione.append(f"La tua tensione e aumentata da {primo.tensione_main}kg a {ultimo.tensione_main}kg — sei migliorato!")
        if ultimo.livello != primo.livello:
            evoluzione.append(f"Sei passato da {primo.livello} a {ultimo.livello} — ottimo progresso!")

    return {
        "utente": nome_utente,
        "totale_setup_salvati": len(storico),
        "primo_setup": {"data": primo.data, "racchetta": primo.racchetta, "tensione": primo.tensione_main},
        "ultimo_setup": {"data": ultimo.data, "racchetta": ultimo.racchetta, "tensione": ultimo.tensione_main},
        "evoluzione": evoluzione,
        "storico_completo": [{"data": e.data, "racchetta": e.racchetta, "corda": e.corda, "tensione_main": e.tensione_main, "tensione_cross": e.tensione_cross, "livello": e.livello} for e in storico]
    }
