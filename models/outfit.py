from sqlalchemy import Column, Integer, String, Float
from database_models import Base

class Outfit(Base):
    __tablename__ = "outfits"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    nome_collezione = Column(String, nullable=False)
    target = Column(String, nullable=False)        # "Maschio", "Femmina", "Bambino"
    stagione = Column(String, nullable=True)      # es: "Primavera/Estate 2026"
    prezzo_totale = Column(Float, nullable=True)
    
    # Capi inclusi nell'outfit
    top = Column(String, nullable=True)           # "T-shirt" o "Polo" (specificare modello/colore)
    pantaloncino_gonna = Column(String, nullable=True) # "Pantaloncini" o "Gonnellino"
    calze = Column(String, nullable=True)
    scarpe = Column(String, nullable=True)         # Collegabile idealmente al modello Scarpa
    cappellino = Column(String, nullable=True)
    borsone = Column(String, nullable=True)        # Collegabile idealmente al modello Borsone
    
    nota = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    def __repr__(self):
        return f"<Outfit {self.brand} {self.nome_collezione} - {self.target}>"
