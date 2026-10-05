from sqlalchemy import Column, Integer, String
from database_models import Base

class Accessorio(Base):
    __tablename__ = "accessori"

    id = Column(Integer, primary_key=True, index=True)

    # Campo richiesto dallo schema Pydantic
    nome = Column(String, nullable=False)

    # Campi presenti nel tuo database
    categoria = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    modello = Column(String, nullable=False)
    colore = Column(String, nullable=False)
    materiale = Column(String, nullable=False)

    # Campi opzionali
    nota = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
