from sqlalchemy import Column, Integer, String, Float
from database_models import Base

class Corda(Base):
    __tablename__ = "corde"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    materiale = Column(String, nullable=True)
    calibro = Column(String, nullable=True)
    rigidita = Column(String, nullable=True)
    colore = Column(String, nullable=True)
    prezzo = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    note = Column(String, nullable=True)