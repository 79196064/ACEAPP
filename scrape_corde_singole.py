import time
import requests
from database_models import SessionLocal
from models.corde import Corda

PEXELS_API_KEY = "a94Pnf4b1GNMuPpB4qmbr07zjU0TbG7D0bVV1kqn3ZKYmgiMNBQ14I0f"
PEXELS_URL = "https://api.pexels.com/v1/search"

def acquisisci_link_immagine(query):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1, "orientation": "square"}
    try:
        risposta = requests.get(PEXELS_URL, headers=headers, params=params, timeout=10)
        if risposta.status_code == 200:
            data = risposta.json()
            photos = data.get("photos", [])
            if photos:
                return photos[0]["src"]["medium"]
    except Exception as e:
        print(f"  Errore: {e}")
    return None

def aggiorna_corde_singole():
    db = SessionLocal()
    corde = db.query(Corda).all()
    print(f"Analisi di {len(corde)} corde (query specifica per ognuna)...")
    contatore = 0
    for c in corde:
        modello = c.model or ""
        query = f"{c.brand} {modello} tennis string".strip()
        link_foto = acquisisci_link_immagine(query)
        if link_foto:
            c.image_url = link_foto[:250]
            contatore += 1
            print(f"  {contatore}/{len(corde)} - {c.brand}: OK")
        else:
            print(f"  {contatore}/{len(corde)} - {c.brand}: NESSUNA IMMAGINE")
        time.sleep(1)
    db.commit()
    db.close()
    print(f"Completato! {contatore} corde aggiornate.")

if __name__ == "__main__":
    aggiorna_corde_singole()
