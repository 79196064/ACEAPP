import time
import requests
from database_models import SessionLocal
from models.racchette import Racchetta

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

def aggiorna_racchette_singole(limite=147):
    db = SessionLocal()
    racchette = db.query(Racchetta).limit(limite).all()
    print(f"Analisi di {len(racchette)} racchette (query specifica per ognuna)...")
    contatore = 0
    for r in racchette:
        query = f"{r.brand} {r.modello} tennis racket"
        link_foto = acquisisci_link_immagine(query)
        if link_foto:
            r.image_url = link_foto[:250]
            contatore += 1
            print(f"  {contatore}/{len(racchette)} - {r.brand} {r.modello}: OK")
        else:
            print(f"  {contatore}/{len(racchette)} - {r.brand} {r.modello}: NESSUNA IMMAGINE")
        time.sleep(1)
    db.commit()
    db.close()
    print(f"Completato! {contatore} racchette aggiornate.")

if __name__ == "__main__":
    aggiorna_racchette_singole()
