import csv
from database_models import SessionLocal
from models.palline import Pallina

db = SessionLocal()
count = 0

with open("data/palline.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing = db.query(Pallina).filter(Pallina.brand == row["brand"], Pallina.modello == row["modello"]).first()
        if existing:
            continue
        db.add(Pallina(
            brand=row["brand"],
            modello=row["modello"],
            superficie=row["superficie"],
            livello=row["livello"],
            pressione=row["pressione"],
            confezione=row["confezione"],
            prezzo=row["prezzo"],
            nota=row["nota"]
        ))
        count += 1

db.commit()
db.close()
print(f"Palline aggiunte: {count}")
