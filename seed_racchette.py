import csv
from database_models import SessionLocal
from models.racchette import Racchetta

CSV_PATH = "data/racchette.csv"

def seed_racchette():
    db = SessionLocal()

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            rac = Racchetta(
                brand=row["racquet_brands"],
                modello=row["racquet_models"],
                peso=300,                 # valore standard
                bilanciamento=32,         # valore standard
                schema_corde="16x19",     # valore standard
                rigidita=65,              # valore standard
                livello="intermedio",     # default
                stile="moderno",          # default
                superficie="terra"        # default
            )
            db.add(rac)

    db.commit()
    db.close()
    print("✔ Seed racchette completato!")

if __name__ == "__main__":
    seed_racchette()
