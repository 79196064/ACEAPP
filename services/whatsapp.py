# services/whatsapp.py
# Servizio WhatsApp Business API - Pronto per Twilio
# Per attivare: inserire TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

import os

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "INSERISCI_QUI")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "INSERISCI_QUI")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

def invia_richiesta_disponibilita(
    negozio_whatsapp: str,
    nome_utente: str,
    racchetta: str,
    corda: str,
    tensione_main: int,
    tensione_cross: int,
    scarpe: str,
    outfit: str,
    antivibro: str,
) -> dict:

    messaggio = f"""
🎾 *Nuova richiesta da ACEAPP*

👤 Cliente: {nome_utente}

🏸 Setup consigliato da ACEAI:
- Racchetta: {racchetta}
- Corda: {corda}
- Tensione: {tensione_main}kg verticali / {tensione_cross}kg orizzontali
- Scarpe: {scarpe}
- Outfit: {outfit}
- Antivibro: {antivibro}

Il cliente vuole verificare la disponibilità.
Rispondi entro 2 minuti! ⚡
    """

    # Modalità simulazione (senza Twilio)
    if TWILIO_ACCOUNT_SID == "INSERISCI_QUI":
        print("SIMULAZIONE WhatsApp:")
        print(f"A: {negozio_whatsapp}")
        print(messaggio)
        return {
            "status": "simulato",
            "destinatario": negozio_whatsapp,
            "messaggio": messaggio
        }

    # Modalità reale (con Twilio)
    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=messaggio,
            to=f"whatsapp:{negozio_whatsapp}"
        )
        return {
            "status": "inviato",
            "sid": message.sid,
            "destinatario": negozio_whatsapp
        }
    except Exception as e:
        return {
            "status": "errore",
            "dettaglio": str(e)
        }
