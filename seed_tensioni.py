from database_models import SessionLocal
from models import Tensione

db = SessionLocal()

tensioni = [
    # PRINCIPIANTE
    {"livello": "principiante", "stile": "piatto", "problemi": "nessuno", "preferenza": "potenza", "kg_verticali": 21, "kg_orizzontali": 21, "nodi": 2},
    {"livello": "principiante", "stile": "arrotatore", "problemi": "nessuno", "preferenza": "comfort", "kg_verticali": 22, "kg_orizzontali": 21, "nodi": 4},
    {"livello": "principiante", "stile": "all-round", "problemi": "gomito", "preferenza": "comfort", "kg_verticali": 20, "kg_orizzontali": 19, "nodi": 2},

    # INTERMEDIO
    {"livello": "intermedio", "stile": "piatto", "problemi": "nessuno", "preferenza": "controllo", "kg_verticali": 23, "kg_orizzontali": 22, "nodi": 4},
    {"livello": "intermedio", "stile": "arrotatore", "problemi": "gomito", "preferenza": "comfort", "kg_verticali": 22, "kg_orizzontali": 21, "nodi": 4},
    {"livello": "intermedio", "stile": "all-round", "problemi": "nessuno", "preferenza": "potenza", "kg_verticali": 22, "kg_orizzontali": 22, "nodi": 2},

    # AVANZATO
    {"livello": "avanzato", "stile": "piatto", "problemi": "nessuno", "preferenza": "controllo", "kg_verticali": 24, "kg_orizzontali": 23, "nodi": 4},
    {"livello": "avanzato", "stile": "arrotatore", "problemi": "nessuno", "preferenza": "controllo", "kg_verticali": 23, "kg_orizzontali": 22, "nodi": 4},
    {"livello": "avanzato", "stile": "all-round", "problemi": "gomito", "preferenza": "comfort", "kg_verticali": 22, "kg_orizzontali": 21, "nodi": 2},
]

for t in tensioni:
    tens = Tensione(**t)
    db.add(tens)

db.commit()
db.close()

print("Tensioni inserite correttamente!")

