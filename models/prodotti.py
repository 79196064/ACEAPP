from sqlalchemy import Column, Integer, String, Float
from database_models import Base

class Prodotto(Base):
    __tablename__ = "prodotti"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    prezzo = Column(Float, nullable=False)
    brand = Column(String, nullable=True)