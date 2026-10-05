import csv
from database_models import SessionLocal
from models.outfit import Outfit

db = SessionLocal()
count = 0

with open("data/outfit.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row["brand"]:
            continue
        existing = db.query(Outfit).filter(Outfit.brand == row["brand"], Outfit.modello == row["modello"]).first()
        if existing:
            continue
        db.add(Outfit(brand=row["brand"], modello=row["modello"], tipo=row["tipo"], colore=row["colore"], materiale=row["materiale"], stagione=row["stagione"], nota=row["nota"]))
        count += 1

db.commit()
db.close()
print(f"Outfit aggiunti: {count}")
