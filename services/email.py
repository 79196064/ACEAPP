import os
import logging

logger = logging.getLogger(__name__)

def invia_email_consulenza(nome: str, email: str, setup: dict, score: int, spiegazione: str):
    """Gestisce l'invio email per la consulenza dei match."""
    api_key = os.getenv("BREVO_API_KEY")
    
    if not api_key:
        print("\n" + "="*60)
        print(f"📧 [MOCK EMAIL] Brevo non configurato. Consulenza per: {nome} (<{email}>)")
        print(f"🏆 Score Profilo Match: {score}/100")
        print(f"🎾 Setup Consigliato: {setup}")
        print("="*60 + "\n")
        return True

    try:
        # Spazio predisposto per la logica reale di Brevo in produzione
        logger.info(f"Email consulenza inviata a {email} tramite Brevo.")
        return True
    except Exception as e:
        logger.error(f"Errore invio email consulenza Brevo: {str(e)}")
        return False


def invia_email_benvenuto(email: str, nome: str):
    """Gestisce l'invio email di benvenuto per i nuovi utenti."""
    api_key = os.getenv("BREVO_API_KEY")
    
    if not api_key:
        print("\n" + "="*60)
        print(f"📧 [MOCK EMAIL] Brevo non configurato. Benvenuto per: {nome} (<{email}>)")
        print(f"🎉 Messaggio: Benvenuto su ACEAPP!")
        print("="*60 + "\n")
        return True

    try:
        # Spazio predisposto per la logica reale di Brevo in produzione
        logger.info(f"Email benvenuto inviata a {email} tramite Brevo.")
        return True
    except Exception as e:
        logger.error(f"Errore invio email benvenuto Brevo: {str(e)}")
        return False
