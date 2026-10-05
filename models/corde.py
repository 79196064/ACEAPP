from sqlalchemy import Column, Integer, String, Float
from database_models import Base

class Corda(Base):
    __tablename__ = "corde"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    materiale = Column(String, nullable=True)
    calibro = Column(String, nullable=True)
    rigidita = Column(String, nullable=True)
    colore = Column(String, nullable=True)
    prezzo = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    note = Column(String, nullable=True)
    forma_sezione = Column(String, nullable=True)
    texture = Column(String, nullable=True)
    rigidita_statica = Column(Float, nullable=True)
    rigidita_dinamica = Column(Float, nullable=True)
    perdita_tensione_percentuale = Column(Float, nullable=True)
    resilienza = Column(Float, nullable=True)
    resistenza_trazione = Column(Float, nullable=True)
    attrito_corda_palla = Column(Float, nullable=True)
    attrito_corda_corda = Column(Float, nullable=True)
    snapback_score = Column(Integer, nullable=True)
    tensione_min_kg = Column(Float, nullable=True)
    tensione_max_kg = Column(Float, nullable=True)
    coating = Column(String, nullable=True)
    durata_snapback_ore = Column(Float, nullable=True)
    compatibilita_ibrido = Column(String, nullable=True)
