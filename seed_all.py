import csv
import os
from database_models import SessionLocal, Base, engine
from models.racchette import Racchetta

Base.metadata.create_all(bind=engine)

DEFAULT_RACKET_IMG = "https://images.unsplash.com/photo-1617083934555-ac7d4fed8814?q=80&w=800&auto=format&fit=crop"

def popola_racchette():
    db = SessionLocal()
    # Cerca il file CSV tra i nomi possibili visibili nel tuo progetto
    possibili_csv = [
        os.path.join("data", "racchette.csv"),
        os.path.join("data", "racquets_1.csv"),
        "racquets_1.csv",
        os.path.join("data", "catalogo_storico.csv")
    ]
    
    csv_trovato = None
    for path in possibili_csv:
        if os.path.exists(path):
            csv_trovato = path
            break

    if not csv_trovato:
        print("Nessun file CSV racchette trovato! Controlla i nomi nella cartella data.")
        db.close()
        return

    print(f"Caricamento dati da: {csv_trovato}...")
    
    count = 0
    with open(csv_trovato, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Adatta le chiavi in base all'intestazione del tuo CSV
            brand = row.get("brand") or row.get("Brand") or row.get("make")
            modello = row.get("modello") or row.get("Modello") or row.get("model")
            
            if not brand or not modello:
                continue

            existing = db.query(Racchetta).filter(
                Racchetta.brand == brand,
                Racchetta.modello == modello
            ).first()

            img = row.get("image_url") if row.get("image_url") else DEFAULT_RACKET_IMG

            if existing:
                existing.image_url = img
            else:
                db.add(Racchetta(
                    brand=brand,
                    modello=modello,
                    prezzo=float(row["prezzo"]) if row.get("prezzo") else 199.0,
                    piatto_corde=int(row["piatto_corde"]) if row.get("piatto_corde") else None,
                    peso=int(row["peso"]) if row.get("peso") else None,
                    image_url=img
                ))
                count += 1

    db.commit()
    db.close()
    print(f"SUCCESS: Importate/Aggiornate {count} racchette nel database!")

if __name__ == "__main__":
    popola_racchette()