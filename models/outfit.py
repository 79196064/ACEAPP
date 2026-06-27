from sqlalchemy import Column, Integer, String
from database_models import Base

class Outfit(Base):
    __tablename__ = "outfit"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=True)
    modello = Column(String, nullable=True)
    tipo = Column(String, nullable=True)
    colore = Column(String, nullable=True)
    materiale = Column(String, nullable=True)
    stagione = Column(String, nullable=True)
    nota = Column(String, nullable=True)
