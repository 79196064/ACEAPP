import json
from database_models import SessionLocal, Base, engine

try:
    from models.racchette import Racchetta
except ImportError:
    try:
        from models.racchetta import Racchetta
    except ImportError:
        from database_models import Racchetta

def safe_int(valore, default=0):
    if valore is None or valore == "" or str(valore).lower() == "none":
        return default
    try:
        return int(float(str(valore).strip()))
    except:
        return default

# Utilizziamo direttamente i dati ispezionati del dataset ufficiale di Racqix
dataset_json = """[
  {"slug":"babolat-aero-112-2005","brand":"Babolat","model":"Aero","year":"2005","weight":null,"swingweight":null,"ra":68,"balance_mm":null,"head_size":112,"string_pattern":"16x19"},
  {"slug":"babolat-aero-g","brand":"Babolat","model":"Aero","year":null,"weight":270,"swingweight":275,"ra":69,"balance_mm":320,"head_size":102,"string_pattern":"16x19"},
  {"slug":"babolat-aero-g-2019","brand":"Babolat","model":"Aero","year":"2019","weight":270,"swingweight":null,"ra":70,"balance_mm":320,"head_size":102,"string_pattern":"16x19"},
  {"slug":"babolat-aero-pro-drive-gt-2010","brand":"Babolat","model":"Aero","year":"2010","weight":300,"swingweight":320,"ra":71,"balance_mm":320,"head_size":100,"string_pattern":"16x19"},
  {"slug":"babolat-pure-aero-100-2026","brand":"Babolat","model":"Pure Aero 100","year":"2026","weight":300,"swingweight":320,"ra":66,"balance_mm":329.9,"head_size":100,"string_pattern":"16x19"},
  {"slug":"head-speed-mp-2024","brand":"Head","model":"Speed","year":"2024","weight":300,"swingweight":320,"ra":63,"balance_mm":320,"head_size":100,"string_pattern":"16x19"},
  {"slug":"head-speed-pro-2026","brand":"Head","model":"Speed","year":"2026","weight":310,"swingweight":320,"ra":66,"balance_mm":320,"head_size":100,"string_pattern":"18x20"},
  {"slug":"wilson-blade-98-16x19-v9-2026","brand":"Wilson","model":"Blade V9 98 16x19","year":"2026","weight":305,"swingweight":324,"ra":62,"balance_mm":320,"head_size":98,"string_pattern":"16x19"},
  {"slug":"wilson-blade-98-18x20-v9-2026","brand":"Wilson","model":"Blade V9 98 18x20","year":"2026","weight":305,"swingweight":330,"ra":60,"balance_mm":320,"head_size":98,"string_pattern":"18x20"},
  {"slug":"wilson-pro-staff-97-v14-0-2023","brand":"Wilson","model":"Pro Staff","year":"2023","weight":315,"swingweight":320,"ra":63,"balance_mm":310,"head_size":97,"string_pattern":"16x19"}
]"""

try:
    items = json.loads(dataset_json)
    print(f"Dataset offline caricato con successo. Inizio popolamento...")
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    caricate = 0
    
    for item in items:
        brand = str(item.get("brand", "Unknown")).strip()
        year = item.get("year")
        model_base = item.get("model", "Unknown")
        
        model_completo = f"{str(model_base).strip()} ({year})" if year else str(model_base).strip()
            
        esiste = db.query(Racchetta).filter_by(brand=brand, modello=model_completo).first()
        if not esiste:
            nuovo = Racchetta(
                brand=brand,
                modello=model_completo,
                piatto_corde=safe_int(item.get("head_size"), 100),
                peso=safe_int(item.get("weight"), 300),
                bilanciamento=safe_int(item.get("balance_mm"), 320),
                schema_corde=str(item.get("string_pattern", "16x19")),
                profilo="N/D",
                rigidita=safe_int(item.get("ra"), 65),
                swingweight=safe_int(item.get("swingweight"), 315),
                livello="intermedio",
                stile="bilanciato",
                superficie="terra"
            )
            db.add(nuovo)
            caricate += 1
            
    db.commit()
    db.close()
    print(f"--- SUCCESSOCERTOSINO: CATALOGO IMPORTATO CON {caricate} MODELLI STRUTTURATI! ---")
except Exception as e:
    print("Errore durante l'esecuzione:", e)
