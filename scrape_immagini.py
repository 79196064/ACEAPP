import time
import requests
from database_models import SessionLocal
from models.racchette import Racchetta
from models.corde import Corda
from models.borsoni import Borsone
from models.palline import Pallina
from models.outfit import Outfit

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

def aggiorna_categoria(db, modello_classe, query_ricerca, limite=200):
    items = db.query(modello_classe).limit(limite).all()
    print(f"Analisi di {len(items)} elementi...")
    link_foto = acquisisci_link_immagine(query_ricerca)
    if link_foto:
        for item in items:
            item.image_url = link_foto[:250]
        print(f"  Link applicato: {link_foto[:60]}")
    else:
        print("  Nessuna immagine trovata")
    time.sleep(1)
    db.commit()

def avvia_scraping_catalogo(limite=200):
    db = SessionLocal()
    print("Avvio ricerca multimediale con Pexels...")
    aggiorna_categoria(db, Racchetta, "tennis racket equipment", limite)
    aggiorna_categoria(db, Corda, "tennis string racket", limite)
    aggiorna_categoria(db, Borsone, "tennis bag sports", limite)
    aggiorna_categoria(db, Pallina, "tennis balls yellow", limite)
    aggiorna_categoria(db, Outfit, "tennis outfit clothing", limite)
    db.close()
    print("Completato!")

if __name__ == "__main__":
    avvia_scraping_catalogo()
