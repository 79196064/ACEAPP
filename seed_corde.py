import csv
from database_models import SessionLocal
from models.corde import Corda

db = SessionLocal()
count = 0

with open("data/corde.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing = db.query(Corda).filter(Corda.brand == row["brand"], Corda.model == row["model"]).first()
        if existing:
            continue
        db.add(Corda(brand=row["brand"], model=row["model"], materiale=row["materiale"], calibro=row["calibro"], rigidita=row["rigidita"], colore=row["colore"], prezzo=row["prezzo"], image_url=row["image_url"], note=row["note"]))
        count += 1

db.commit()
db.close()
print(f"Corde aggiunte: {count}")
