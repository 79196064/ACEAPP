from sqlalchemy import Column, Integer, String
from database_models import Base

class Accessorio(Base):
    __tablename__ = "accessori"

    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    modello = Column(String, nullable=False)
    colore = Column(String, nullable=False)
    materiale = Column(String, nullable=False)
    dimensione = Column(String, nullable=False)
    nota = Column(String, nullable=True)
    image_url = Column(String, nullable=True)