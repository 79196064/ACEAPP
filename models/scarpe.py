from sqlalchemy import Column, Integer, String
from database_models import Base

class Scarpa(Base):
    __tablename__ = "scarpe"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    superficie = Column(String, nullable=True)
    stabilita = Column(String, nullable=True)
    ammortizzazione = Column(String, nullable=True)
    peso = Column(Integer, nullable=True)
    drop = Column(Integer, nullable=True)
    colore = Column(String, nullable=True)
    note = Column(String, nullable=True)
