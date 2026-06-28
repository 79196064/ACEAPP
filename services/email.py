import os
import requests

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

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
            <body style="font-family: Arial, sans-serif; background-color: #1A2E4C; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #C05A00; padding: 30px; border-radius: 10px;">
                    <h1 style="color: white; text-align: center;">ACEAPP TENNIS</h1>
                    <h2 style="color: white;">Ciao {nome}!</h2>
                    <p style="color: white; font-size: 16px;">
                        Benvenuto in ACEAPP - la prima piattaforma tennis con intelligenza artificiale!
                    </p>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://aceapp.it" style="background-color: #1A2E4C; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">
                            Scopri ACEAPP
                        </a>
                    </div>
                    <p style="color: white; margin-top: 30px; font-size: 12px; text-align: center;">
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
            print(f"Email inviata a {email}")
            return True
        else:
            print(f"Errore Brevo: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Errore email: {str(e)}")
        return False