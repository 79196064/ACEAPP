from sqlalchemy import Column, Integer, String
from database_models import Base

class Utente(Base):
    __tablename__ = "utenti"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    ruolo = Column(String, nullable=False, default="utente", server_default="utente")
