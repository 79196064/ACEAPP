"""Collega un negozio esistente al relativo gestore.

Esempio: python assegna_proprietario_negozio.py 1 gestore@negozio.it
"""

import argparse

from database_models import SessionLocal
from models.negozi import Negozio
from models.utenti import Utente


def main() -> None:
    parser = argparse.ArgumentParser(description="Assegna un gestore a un negozio ACEAPP")
    parser.add_argument("negozio_id", type=int)
    parser.add_argument("email_gestore")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        negozio = db.query(Negozio).filter(Negozio.id == args.negozio_id).first()
        if not negozio:
            raise SystemExit("Negozio non trovato")
        utente = db.query(Utente).filter(
            Utente.email == args.email_gestore.lower().strip()
        ).first()
        if not utente:
            raise SystemExit("Utente gestore non trovato")

        utente.ruolo = "negozio"
        negozio.proprietario_id = utente.id
        db.commit()
        print(f"Gestore assegnato: {utente.email} -> {negozio.nome}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
