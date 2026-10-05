from sqlalchemy import Column, Integer, String, Float
from database_models import Base

class Tensione(Base):
    __tablename__ = "tensioni"

    id = Column(Integer, primary_key=True, index=True)
    livello = Column(String, nullable=False)
    stile = Column(String, nullable=False)
    problemi = Column(String, nullable=False)
    preferenza = Column(String, nullable=False)
    kg_verticali = Column(Float, nullable=False)
    kg_orizzontali = Column(Float, nullable=False)
    nodi = Column(Integer, nullable=False)
