import csv
from database_models import SessionLocal
from models.accessori import Accessorio

db = SessionLocal()
count = 0

with open("data/accessori.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing = db.query(Accessorio).filter(Accessorio.brand == row["brand"], Accessorio.modello == row["modello"]).first()
        if existing:
            continue
        db.add(Accessorio(categoria=row["categoria"], brand=row["brand"], modello=row["modello"], colore=row["colore"], materiale=row["materiale"], dimensione=row["dimensione"], nota=row["nota"], image_url=row["image_url"]))
        count += 1

db.commit()
db.close()
print(f"Accessori aggiunti: {count}")
