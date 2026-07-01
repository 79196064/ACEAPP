import os
import requests

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
LOGO_URL = "https://i.postimg.cc/dQRjwN4W/f6250d37-8939-4955-836c-7c09e4aee4ba.jpg"

def invia_email_benvenuto(nome: str, email: str):
    BREVO_SMTP_KEY = os.getenv("BREVO_SMTP_KEY")
    if not BREVO_SMTP_KEY:
        print("Brevo API key non configurata")
        return False
    try:
        payload = {
            "sender": {"name": "ACEAPP Team", "email": "info@aceapp.it"},
            "to": [{"email": email, "name": nome}],
            "subject": "Benvenuto in ACEAPP!",
            "htmlContent": f"""<html>
            <body style="font-family: Arial, sans-serif; background-color: #1A2E4C; padding: 20px; margin: 0;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #1A2E4C; padding: 30px; border-radius: 10px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="{LOGO_URL}" alt="ACEAPP Logo" style="width: 120px; height: 120px; border-radius: 50%;"/>
                    </div>
                    <div style="background-color: #C05A00; padding: 30px; border-radius: 10px;">
                        <h1 style="color: white; text-align: center; margin: 0 0 20px 0;">ACEAPP TENNIS</h1>
                        <h2 style="color: white; margin: 0 0 15px 0;">Ciao {nome}!</h2>
                        <p style="color: white; font-size: 16px; line-height: 1.6;">
                            Benvenuto in ACEAPP - la prima piattaforma tennis con algoritmo biometrico ACEAI!
                        </p>
                        <p style="color: white; font-size: 16px; line-height: 1.6;">
                            Il nostro algoritmo ACEAI analizzera il tuo profilo fisico e ti consigliera
                            l'attrezzatura perfetta per il tuo stile di gioco.
                        </p>
                        <div style="text-align: center; margin-top: 30px;">
                            <a href="https://aceapp.it"
                               style="background-color: #1A2E4C; color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 16px; display: inline-block;">
                                Scopri ACEAPP
                            </a>
                        </div>
                    </div>
                    <p style="color: rgba(255,255,255,0.5); margin-top: 20px; font-size: 12px; text-align: center;">
                        2026 ACEAPP Tennis - info@aceapp.it
                    </p>
                </div>
            </body>
            </html>"""
        }
        headers = {
            "accept": "application/json",
            "api-key": BREVO_SMTP_KEY,
            "content-type": "application/json"
        }
        response = requests.post(BREVO_API_URL, json=payload, headers=headers)
        if response.status_code == 201:
            print(f"Email benvenuto inviata a {email}")
            return True
        else:
            print(f"Errore Brevo benvenuto: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Errore email benvenuto: {str(e)}")
        return False


def invia_email_consulenza(nome: str, email: str, setup: dict, score: float, spiegazione: str):
    BREVO_SMTP_KEY = os.getenv("BREVO_SMTP_KEY")
    if not BREVO_SMTP_KEY:
        print("Brevo API key non configurata")
        return False
    try:
        racchetta = setup.get("racchetta", {}) or {}
        corde = setup.get("corde", {}) or {}
        tensione = setup.get("tensione", {}) or {}
        palline = setup.get("palline", {}) or {}

        payload = {
            "sender": {"name": "ACEAPP Team", "email": "info@aceapp.it"},
            "to": [{"email": email, "name": nome}],
            "subject": "Il tuo setup ACEAI personalizzato e' pronto!",
            "htmlContent": f"""<html>
            <body style="font-family: Arial, sans-serif; background-color: #1A2E4C; padding: 20px; margin: 0;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="{LOGO_URL}" alt="ACEAPP Logo" style="width: 100px; height: 100px; border-radius: 50%;"/>
                    </div>
                    <div style="background-color: #C05A00; padding: 25px; border-radius: 10px; margin-bottom: 15px;">
                        <h1 style="color: white; text-align: center; margin: 0 0 10px 0;">ACEAPP TENNIS</h1>
                        <h2 style="color: white; margin: 0 0 15px 0;">Ciao {nome}!</h2>
                        <p style="color: white; font-size: 16px;">
                            ACEAI ha analizzato il tuo profilo e ha trovato il setup perfetto per te!
                        </p>
                        <div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; text-align: center;">
                            <span style="color: #FFD700; font-size: 28px; font-weight: bold;">Score ACEAI: {score:.1f}/100</span>
                        </div>
                    </div>
                    <div style="background-color: #1A2E4C; border: 1px solid #C05A00; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                        <h3 style="color: #C05A00; margin: 0 0 15px 0;">Il tuo Setup Consigliato</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <td style="color: rgba(255,255,255,0.7); padding: 8px 0;">Racchetta</td>
                                <td style="color: white; font-weight: bold; padding: 8px 0;">{racchetta.get('brand', '')} {racchetta.get('modello', '')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <td style="color: rgba(255,255,255,0.7); padding: 8px 0;">Corda</td>
                                <td style="color: white; font-weight: bold; padding: 8px 0;">{corde.get('nome', '')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <td style="color: rgba(255,255,255,0.7); padding: 8px 0;">Tensione</td>
                                <td style="color: white; font-weight: bold; padding: 8px 0;">{tensione.get('verticali', '')} / {tensione.get('orizzontali', '')} kg</td>
                            </tr>
                            <tr>
                                <td style="color: rgba(255,255,255,0.7); padding: 8px 0;">Palline</td>
                                <td style="color: white; font-weight: bold; padding: 8px 0;">{palline.get('brand', '')} {palline.get('modello', '')}</td>
                            </tr>
                        </table>
                    </div>
                    <div style="background-color: #1A2E4C; border: 1px solid #C05A00; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                        <h3 style="color: #C05A00; margin: 0 0 10px 0;">Analisi ACEAI</h3>
                        <p style="color: white; font-size: 14px; line-height: 1.6;">{spiegazione[:500]}</p>
                    </div>
                    <div style="background-color: #FFD700; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                        <h3 style="color: #1A2E4C; margin: 0 0 5px 0;">Il tuo Codice Sconto</h3>
                        <div style="font-size: 32px; font-weight: bold; color: #1A2E4C; letter-spacing: 5px;">ACEAI10</div>
                        <p style="color: #1A2E4C; margin: 5px 0 0 0; font-size: 13px;">10% di sconto nei negozi partner ACEAPP</p>
                    </div>
                    <div style="text-align: center; margin-bottom: 20px;">
                        <a href="https://aceapp.it"
                           style="background-color: #C05A00; color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 16px; display: inline-block;">
                            Trova il Negozio Piu Vicino
                        </a>
                    </div>
                    <p style="color: rgba(255,255,255,0.5); font-size: 12px; text-align: center;">
                        2026 ACEAPP Tennis - info@aceapp.it
                    </p>
                </div>
            </body>
            </html>"""
        }
        headers = {
            "accept": "application/json",
            "api-key": BREVO_SMTP_KEY,
            "content-type": "application/json"
        }
        response = requests.post(BREVO_API_URL, json=payload, headers=headers)
        if response.status_code == 201:
            print(f"Email consulenza inviata a {email}")
            return True
        else:
            print(f"Errore Brevo consulenza: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Errore email consulenza: {str(e)}")
        return False