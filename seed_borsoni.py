import csv
from database_models import SessionLocal
from models.borsoni import Borsone

db = SessionLocal()
count = 0

with open("data/borsoni_tennis.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing = db.query(Borsone).filter(Borsone.marca == row["marca"], Borsone.modello == row["modello"]).first()
        if existing:
            continue
        db.add(Borsone(marca=row["marca"], modello=row["modello"], tipo=row["tipo"], capacita_litri=row["capacita_litri"], numero_racchette=row["numero_racchette"], scomparti=row["scomparti"], tasca_termica=row["tasca_termica"], materiale=row["materiale"], colori=row["colori"], prezzo=row["prezzo"], paese_origine=row["paese_origine"], fascia=row["fascia"]))
        count += 1

db.commit()
db.close()
print(f"Borsoni aggiunti: {count}")
