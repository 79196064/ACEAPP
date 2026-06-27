from sqlalchemy import Column, Integer, String, Float
from database_models import Base

class Borsone(Base):
    __tablename__ = "borsoni"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modello = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    capacita_litri = Column(String, nullable=False)
    numero_racchette = Column(String, nullable=False)
    scomparti = Column(String, nullable=False)
    tasca_termica = Column(String, nullable=False)
    materiale = Column(String, nullable=False)
    colori = Column(String, nullable=False)
    prezzo = Column(String, nullable=False)
    paese_origine = Column(String, nullable=False)
    fascia = Column(String, nullable=False)
