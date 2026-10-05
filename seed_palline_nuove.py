from database_models import SessionLocal
from models.palline import Pallina

db = SessionLocal()

palline_data = [
    {"brand": "Wilson", "modello": "US Open", "superficie": "cemento", "livello": "avanzato", "pressione": "pressurizzata", "confezione": "3", "prezzo": "5.99", "nota": "Pallina ufficiale US Open"},
    {"brand": "Wilson", "modello": "Triniti", "superficie": "cemento", "livello": "intermedio", "pressione": "ibrida", "confezione": "3", "prezzo": "12.99", "nota": "Tecnologia innovativa, dura piu a lungo"},
    {"brand": "Penn", "modello": "Championship Extra Duty", "superficie": "cemento", "livello": "principiante", "pressione": "pressurizzata", "confezione": "3", "prezzo": "4.99", "nota": "Pallina piu venduta in America"},
]

palline_data += [
    {"brand": "Penn", "modello": "Tour", "superficie": "cemento", "livello": "avanzato", "pressione": "pressurizzata", "confezione": "3", "prezzo": "6.99", "nota": "Usata in tornei ATP"},
    {"brand": "Head", "modello": "Tour", "superficie": "cemento", "livello": "intermedio", "pressione": "pressurizzata", "confezione": "3", "prezzo": "5.49", "nota": "Molto diffusa in Europa"},
    {"brand": "Dunlop", "modello": "Fort All Court", "superficie": "cemento", "livello": "intermedio", "pressione": "pressurizzata", "confezione": "4", "prezzo": "7.99", "nota": "La piu usata nei club UK"},
    {"brand": "Dunlop", "modello": "Fort Clay Court", "superficie": "terra", "livello": "intermedio", "pressione": "pressurizzata", "confezione": "4", "prezzo": "7.99", "nota": "Specifica per terra rossa"},
    {"brand": "Babolat", "modello": "Gold", "superficie": "terra", "livello": "avanzato", "pressione": "pressurizzata", "confezione": "3", "prezzo": "6.49", "nota": "Qualita premium"},
    {"brand": "Babolat", "modello": "Team", "superficie": "cemento", "livello": "intermedio", "pressione": "pressurizzata", "confezione": "4", "prezzo": "5.99", "nota": "Buon livello intermedio"},
    {"brand": "Tecnifibre", "modello": "X-One", "superficie": "cemento", "livello": "avanzato", "pressione": "pressurizzata", "confezione": "3", "prezzo": "6.99", "nota": "Ottima durata, brand emergente"},
    {"brand": "Head", "modello": "Championship", "superficie": "cemento", "livello": "principiante", "pressione": "pressurizzata", "confezione": "4", "prezzo": "5.49", "nota": "Buon rapporto qualita prezzo"},
    {"brand": "Wilson", "modello": "Roland Garros", "superficie": "terra", "livello": "avanzato", "pressione": "pressurizzata", "confezione": "3", "prezzo": "8.99", "nota": "Ufficiale terra rossa Roland Garros"},
    {"brand": "Dunlop", "modello": "ATP", "superficie": "cemento", "livello": "avanzato", "pressione": "pressurizzata", "confezione": "3", "prezzo": "7.49", "nota": "Ufficiale tour ATP"},
    {"brand": "Penn", "modello": "Marathon", "superficie": "cemento", "livello": "intermedio", "pressione": "pressurizzata", "confezione": "3", "prezzo": "6.49", "nota": "Ex ufficiale ATP"},
    {"brand": "Slazenger", "modello": "Wimbledon", "superficie": "erba", "livello": "avanzato", "pressione": "pressurizzata", "confezione": "4", "prezzo": "9.99", "nota": "Ufficiale Wimbledon"},
]

for p in palline_data:
    esistente = db.query(Pallina).filter(
        Pallina.brand == p["brand"],
        Pallina.modello == p["modello"]
    ).first()
    if not esistente:
        nuova = Pallina(**p)
        db.add(nuova)
        print(f"Aggiunta: {p['brand']} {p['modello']}")

db.commit()
db.close()
print("Completato!")
