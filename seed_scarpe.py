import csv
from database_models import SessionLocal
from models.scarpe import Scarpa

db = SessionLocal()
count = 0

with open("data/scarpe.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row["brand"]:
            continue
        existing = db.query(Scarpa).filter(Scarpa.brand == row["brand"], Scarpa.model == row["model"]).first()
        if existing:
            continue
        db.add(Scarpa(brand=row["brand"], model=row["model"], superficie=row["superficie"], stabilita=row["stabilita"], ammortizzazione=row["ammortizzazione"], peso=int(row["peso"]), drop=int(row["drop"]), colore=row["colore"], note=row["note"]))
        count += 1

db.commit()
db.close()
print(f"Scarpe aggiunte: {count}")
