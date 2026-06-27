from sqlalchemy import Column, Integer, String
from database_models import Base

class Pallina(Base):
    __tablename__ = "palline"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    modello = Column(String, nullable=False)
    superficie = Column(String, nullable=False)
    livello = Column(String, nullable=False)
    pressione = Column(String, nullable=True)
    confezione = Column(String, nullable=True)
    prezzo = Column(String, nullable=True)
    nota = Column(String, nullable=True)
