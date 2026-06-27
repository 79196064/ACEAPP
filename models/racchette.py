from sqlalchemy import Column, Integer, String
from database_models import Base

class Racchetta(Base):
    __tablename__ = "racchette"
    ...


    id = Column(Integer, primary_key=True, index=True)

    brand = Column(String, nullable=False)
    modello = Column(String, nullable=False)

    peso = Column(Integer, nullable=True)              # in grammi
    bilanciamento = Column(Integer, nullable=True)     # in cm
    schema_corde = Column(String, nullable=True)       # es: "16x19"
    rigidita = Column(Integer, nullable=True)          # RA

    # opzionale: per filtrare meglio
    livello = Column(String, nullable=True)            # es: "intermedio"
    stile = Column(String, nullable=True)              # es: "arrotino"
    superficie = Column(String, nullable=True)         # es: "terra"

    def __repr__(self):
        return f"<Racchetta {self.brand} {self.modello}>"
