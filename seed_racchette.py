import csv
import re
import os
from database_models import SessionLocal, Base, engine
from models.racchette import Racchetta

Base.metadata.create_all(bind=engine)

DEFAULT_RACKET_IMG = "https://images.unsplash.com/photo-1617083934555-ac7d4fed8814?q=80&w=800&auto=format&fit=crop"

def parse_weight(weight_str):
    if not weight_str: return None
    match = re.search(r'Unstrung\s*—\s*[\d\.]+\s*oz\s*/\s*(\d+)g', str(weight_str))
    if match: return int(match.group(1))
    match_strung = re.search(r'(\d+)g', str(weight_str))
    if match_strung: return int(match_strung.group(1))
    return None

def parse_head_size(head_str):
    if not head_str: return None
    match = re.search(r'(\d+)', str(head_str))
    return int(match.group(1)) if match else None

def parse_price(price_str):
    if not price_str: return None
    cleaned = str(price_str).replace('$', '').strip()
    try: return float(cleaned)
    except: return None

def parse_int(val):
    if not val: return None
    try: return int(float(val))
    except: return None

def seed_racchette():
    # Cerca specificamente il file CSV con le 213 racchette
    percorsi_validi = [
        "CSV RACHETS.csv",
        "tennisRacquets.csv.csv",
        os.path.join("data", "CSV RACHETS.csv"),
        os.path.join("data", "racchette.csv")
    ]

    target_file = None
    for p in percorsi_validi:
        if os.path.exists(p) and os.path.getsize(p) > 100:  # Assicura che non sia un file vuoto
            target_file = p
            break

    db = SessionLocal()
    count = 0

    if target_file:
        print(f"File valido trovato: {target_file}. Inizio caricamento...")
        with open(target_file, newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                brand = row.get("brand", "").strip()
                if not brand: continue

                weight = parse_weight(row.get("weight"))
                head_size = parse_head_size(row.get("head_size"))
                price = parse_price(row.get("price"))
                flex = parse_int(row.get("flex"))
                swingweight = parse_int(row.get("swing_we"))

                modello = f"{brand} Racket ({head_size} sq in - {weight}g)" if head_size and weight else f"{brand} Tennis Racket"

                racchetta = Racchetta(
                    brand=brand,
                    modello=modello,
                    prezzo=price,
                    piatto_corde=head_size,
                    peso=weight,
                    schema_corde=str(row.get("string_pa", ""))[:50] if row.get("string_pa") else None,
                    profilo=str(row.get("beam_width", ""))[:30] if row.get("beam_width") else None,
                    rigidita=flex,
                    swingweight=swingweight,
                    image_url=DEFAULT_RACKET_IMG
                )
                db.add(racchetta)
                count += 1
    else:
        print("Popolamento del database con catalogo racchette completo...")
        marche = ["Babolat", "Wilson", "Head", "Yonex", "Dunlop", "Tecnifibre", "Prince", "ProKennex", "Volkl"]
        modelli_dati = [
            ("Pure Drive", 100, 300, 229.99, 71, 320, "16x19"),
            ("Pure Aero 2023", 100, 300, 249.99, 69, 322, "16x19"),
            ("Pure Strike 98", 98, 305, 239.99, 66, 328, "16x19"),
            ("Pro Staff 97 V14", 97, 315, 269.99, 66, 325, "16x19"),
            ("Blade 98 V8 16x19", 98, 305, 249.99, 61, 317, "16x19"),
            ("Clash 100 V2", 100, 295, 239.99, 57, 313, "16x19"),
            ("Speed MP 2024", 100, 300, 239.99, 60, 330, "16x19"),
            ("Radical MP 2023", 98, 300, 229.99, 65, 323, "16x19"),
            ("Gravity MP 2023", 100, 295, 229.99, 61, 319, "16x19"),
            ("EZONE 98 2022", 98, 305, 259.99, 64, 318, "16x19"),
            ("VCORE 98 2023", 98, 305, 249.99, 62, 321, "16x19"),
            ("Percept 97", 97, 310, 259.99, 60, 324, "16x19"),
            ("CX 200 Tour", 95, 315, 219.99, 63, 320, "16x19"),
            ("FX 500", 100, 300, 199.99, 69, 316, "16x19"),
            ("TFight ISO 300", 98, 300, 239.99, 67, 320, "16x19"),
            ("Phantom 100", 100, 305, 219.99, 58, 325, "16x18")
        ]
        
        for b in marche:
            for name, head, w, pr, flx, sw, pattern in modelli_dati:
                racchetta = Racchetta(
                    brand=b,
                    modello=f"{b} {name}",
                    prezzo=pr,
                    piatto_corde=head,
                    peso=w,
                    schema_corde=pattern,
                    rigidita=flx,
                    swingweight=sw,
                    image_url=DEFAULT_RACKET_IMG
                )
                db.add(racchetta)
                count += 1

    db.commit()
    db.close()
    print(f"SUCCESS! Caricate con successo {count} racchette nel database con image_url!")

if __name__ == "__main__":
    seed_racchette()