from sqlalchemy import Column, Integer, String, DateTime, Float
from database_models import Base
from datetime import datetime

class RichiestaShop(Base):
    __tablename__ = "richieste_shop"

    id = Column(Integer, primary_key=True, index=True)
    negozio_id = Column(Integer, nullable=False)
    negozio_citta = Column(String, nullable=False)
    prodotto_tipo = Column(String, nullable=False)
    prodotto_nome = Column(String, nullable=False)
    livello_utente = Column(String, nullable=True)
    stile_utente = Column(String, nullable=True)
    superficie = Column(String, nullable=True)
    data = Column(String, nullable=False, default=datetime.now().strftime("%Y-%m-%d"))
    ora = Column(String, nullable=False, default=datetime.now().strftime("%H:%M"))
