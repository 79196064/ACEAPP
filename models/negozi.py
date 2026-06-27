from sqlalchemy import Column, Integer, String, Boolean, Float
from database_models import Base

class Negozio(Base):
    __tablename__ = "negozi"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    citta = Column(String, nullable=False)
    indirizzo = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    email = Column(String, nullable=True)
    sito_web = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    foto_negozio_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)
    superficie_campi = Column(String, nullable=True)
    servizi = Column(String, nullable=True)
    fascia_prezzi = Column(String, nullable=True)
    latitudine = Column(Float, nullable=True)
    longitudine = Column(Float, nullable=True)
    regione = Column(String, nullable=True)
    attivo = Column(Boolean, default=True)
