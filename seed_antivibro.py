from database_models import SessionLocal
from models import Antivibro

db = SessionLocal()

antivibros = [
    {"nome": "Wilson Shock Shield", "brand": "Wilson", "forma": "tondo", "rigidita": 4, "materiale": "silicone", "colore": "nero", "prezzo": 6.90},
    {"nome": "Babolat Custom Damp", "brand": "Babolat", "forma": "a smile", "rigidita": 5, "materiale": "gomma", "colore": "giallo", "prezzo": 7.90},
    {"nome": "Head Smartsorb", "brand": "Head", "forma": "a T", "rigidita": 6, "materiale": "silicone", "colore": "trasparente", "prezzo": 8.50},
    {"nome": "Yonex Vibration Stopper", "brand": "Yonex", "forma": "tondo", "rigidita": 3, "materiale": "gomma", "colore": "blu", "prezzo": 5.90},
    {"nome": "Tecnifibre Vibra Clip", "brand": "Tecnifibre", "forma": "clip", "rigidita": 7, "materiale": "silicone", "colore": "rosso", "prezzo": 9.90},
    {"nome": "Prince Silencer", "brand": "Prince", "forma": "a smile", "rigidita": 4, "materiale": "gomma", "colore": "verde", "prezzo": 6.50},
]

for a in antivibros:
    antivibro = Antivibro(**a)
    db.add(antivibro)

db.commit()
db.close()

print("Antivibratori inseriti correttamente!")

