from sqlalchemy import Column, Integer, String, Float

from database_models import Base

class Racchetta(Base):
    __tablename__ = "racchette"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    modello = Column(String, nullable=False)
    prezzo = Column(Float, nullable=True)
    piatto_corde = Column(Integer, nullable=True)      # Aggiunto
    peso = Column(Integer, nullable=True)              # in grammi
    bilanciamento = Column(Integer, nullable=True)     # in mm o cm
    schema_corde = Column(String, nullable=True)       # es: "16x19"
    profilo = Column(String, nullable=True)            # Aggiunto
    rigidita = Column(Integer, nullable=True)          # RA
    swingweight = Column(Integer, nullable=True)       # Aggiunto
    livello = Column(String, nullable=True)            # es: "intermedio"
    stile = Column(String, nullable=True)              # es: "attaccante"
    superficie = Column(String, nullable=True)         # es: "terra"
    image_url = Column(String, nullable=True)          # URL dell'immagine

    def __repr__(self):
        return f"<Racchetta {self.brand} {self.modello}>"
