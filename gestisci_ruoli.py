"""Assegna ruoli a utenti esistenti.

Esempio: python gestisci_ruoli.py admin@aceapp.it admin
"""

import argparse

from database_models import SessionLocal
from models.utenti import Utente

RUOLI_VALIDI = {"utente", "negozio", "admin"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Assegna un ruolo ACEAPP a un utente")
    parser.add_argument("email")
    parser.add_argument("ruolo", choices=sorted(RUOLI_VALIDI))
    args = parser.parse_args()

    db = SessionLocal()
    try:
        utente = db.query(Utente).filter(Utente.email == args.email.lower().strip()).first()
        if not utente:
            raise SystemExit("Utente non trovato")
        utente.ruolo = args.ruolo
        db.commit()
        print(f"Ruolo aggiornato: {utente.email} -> {utente.ruolo}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
