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
            <body style="font-family: Arial, sans-serif; background-color: #1A2E4C; padding: 20px; margin: 0;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #1A2E4C; padding: 30px; border-radius: 10px;">
                    
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="https://i.imgur.com/PEck7c9.jpeg" 
                             alt="ACEAPP Logo" 
                             style="width: 120px; height: 120px; border-radius: 50%;"
                             onerror="this.style.display='none'"/>
                    </div>

                    <div style="background-color: #C05A00; padding: 30px; border-radius: 10px;">
                        <h1 style="color: white; text-align: center; margin: 0 0 20px 0;">ACEAPP TENNIS</h1>
                        <h2 style="color: white; margin: 0 0 15px 0;">Ciao {nome}!</h2>
                        <p style="color: white; font-size: 16px; line-height: 1.6;">
                            Benvenuto in ACEAPP — la prima piattaforma tennis con algoritmo biometrico ACEAI!
                        </p>
                        <p style="color: white; font-size: 16px; line-height: 1.6;">
                            Il nostro algoritmo ACEAI analizzerà il tuo profilo fisico e ti consiglierà 
                            l'attrezzatura perfetta per il tuo stile di gioco.
                        </p>
                        <div style="text-align: center; margin-top: 30px;">
                            <a href="https://aceapp.it" 
                               style="background-color: #1A2E4C; color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 16px; display: inline-block;">
                                Scopri ACEAPP →
                            </a>
                        </div>
                    </div>

                    <p style="color: rgba(255,255,255,0.5); margin-top: 20px; font-size: 12px; text-align: center;">
                        © 2026 ACEAPP Tennis — info@aceapp.it
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
