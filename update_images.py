from sqlalchemy.orm import Session
from database_models import SessionLocal
from models.racchette import Racchetta

BASE_URL = "https://aceapp-backend.onrender.com/static/racchette/"

def aggiorna_immagini():
    db: Session = SessionLocal()

    racchette = db.query(Racchetta).all()
    aggiornate = 0

    for rac in racchette:
        filename = f"{rac.brand}_{rac.modello}".lower().replace(" ", "_") + ".png"
        rac.image_url = BASE_URL + filename
        db.add(rac)
        aggiornate += 1

    db.commit()
    db.close()

    return {"status": "ok", "updated": aggiornate}


if __name__ == "__main__":
    print(aggiorna_immagini())
