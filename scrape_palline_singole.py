import time
import requests
from database_models import SessionLocal
from models.palline import Pallina

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

def aggiorna_palline_singole():
    db = SessionLocal()
    palline = db.query(Pallina).all()
    print(f"Analisi di {len(palline)} palline (query specifica per ognuna)...")
    contatore = 0
    for p in palline:
        query = f"{p.brand} {p.modello} tennis balls"
        link_foto = acquisisci_link_immagine(query)
        if link_foto:
            p.image_url = link_foto[:250]
            contatore += 1
            print(f"  {contatore}/{len(palline)} - {p.brand} {p.modello}: OK")
        else:
            print(f"  {contatore}/{len(palline)} - {p.brand} {p.modello}: NESSUNA IMMAGINE")
        time.sleep(1)
    db.commit()
    db.close()
    print(f"Completato! {contatore} palline aggiornate.")

if __name__ == "__main__":
    aggiorna_palline_singole()
