from sqlalchemy import Column, Integer, String, Float
from database_models import Base

class Antivibro(Base):
    __tablename__ = "antivibro"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    forma = Column(String, nullable=False)
    rigidita = Column(Integer, nullable=False)
    materiale = Column(String, nullable=False)
    colore = Column(String, nullable=False)
    prezzo = Column(Float, nullable=False)
