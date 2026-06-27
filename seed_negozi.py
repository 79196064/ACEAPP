from database_models import SessionLocal
from models.negozi import Negozio

db = SessionLocal()
count = 0

negozi = [
    Negozio(nome="Tennis Club Milano", citta="Milano", indirizzo="Via Roma 1", telefono="+39 02 1234567", whatsapp="+39 335 1234567", email="info@tcmilano.it", sito_web="www.tcmilano.it", logo_url="", foto_negozio_url="", superficie_campi="terra,cemento", servizi="vendita,cordatura,lezioni", fascia_prezzi="premium", attivo=True),
    Negozio(nome="Sport Tennis Roma", citta="Roma", indirizzo="Via Appia 10", telefono="+39 06 9876543", whatsapp="+39 347 9876543", email="info@sporttennisroma.it", sito_web="www.sporttennisroma.it", logo_url="", foto_negozio_url="", superficie_campi="terra", servizi="vendita,cordatura", fascia_prezzi="medio", attivo=True),
    Negozio(nome="Ace Tennis Torino", citta="Torino", indirizzo="Corso Francia 5", telefono="+39 011 5556666", whatsapp="+39 333 5556666", email="info@acetorino.it", sito_web="www.acetorino.it", logo_url="", foto_negozio_url="", superficie_campi="cemento,indoor", servizi="vendita,cordatura,lezioni", fascia_prezzi="medio", attivo=True),
    Negozio(nome="Tennis Shop Napoli", citta="Napoli", indirizzo="Via Toledo 20", telefono="+39 081 3334444", whatsapp="+39 320 3334444", email="info@tennisnapoli.it", sito_web="", logo_url="", foto_negozio_url="", superficie_campi="terra", servizi="vendita", fascia_prezzi="base", attivo=True),
    Negozio(nome="Pro Tennis Firenze", citta="Firenze", indirizzo="Viale Toscana 8", telefono="+39 055 7778888", whatsapp="+39 348 7778888", email="info@protennisfirenze.it", sito_web="www.protennisfirenze.it", logo_url="", foto_negozio_url="", superficie_campi="terra,cemento", servizi="vendita,cordatura,lezioni", fascia_prezzi="premium", attivo=True),
]

for negozio in negozi:
    existing = db.query(Negozio).filter(Negozio.nome == negozio.nome, Negozio.citta == negozio.citta).first()
    if existing:
        continue
    db.add(negozio)
    count += 1

db.commit()
db.close()
print(f"Negozi aggiunti: {count}")
