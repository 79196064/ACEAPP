from database_models import SessionLocal
from models import Prodotto

db = SessionLocal()

racchette = [
    {"nome": "Babolat Pure Drive 2024", "categoria": "racchetta", "prezzo": 229.90, "brand": "Babolat"},
    {"nome": "Babolat Pure Aero 2023", "categoria": "racchetta", "prezzo": 239.90, "brand": "Babolat"},
    {"nome": "Wilson Blade 98 v9", "categoria": "racchetta", "prezzo": 259.90, "brand": "Wilson"},
    {"nome": "Wilson Pro Staff 97 v14", "categoria": "racchetta", "prezzo": 279.90, "brand": "Wilson"},
    {"nome": "Head Speed MP 2024", "categoria": "racchetta", "prezzo": 249.90, "brand": "Head"},
    {"nome": "Head Radical MP 2024", "categoria": "racchetta", "prezzo": 239.90, "brand": "Head"},
    {"nome": "Yonex Ezone 100 2024", "categoria": "racchetta", "prezzo": 259.90, "brand": "Yonex"},
    {"nome": "Yonex VCore 98 2023", "categoria": "racchetta", "prezzo": 249.90, "brand": "Yonex"},
]

for r in racchette:
    prodotto = Prodotto(**r)
    db.add(prodotto)

db.commit()
db.close()

print("Racchette inserite correttamente!")

