import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BREVO_SMTP_KEY = os.getenv("BREVO_SMTP_KEY")
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USER = "info@aceapp.it"

def invia_email_benvenuto(nome: str, email: str):
    if not BREVO_SMTP_KEY:
        print("Brevo SMTP key non configurata")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Benvenuto in ACEAPP! 🎾"
        msg["From"] = f"ACEAPP Team <info@aceapp.it>"
        msg["To"] = email

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #1A2E4C; color: white; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #C05A00; padding: 30px; border-radius: 10px;">
                <h1 style="color: white; text-align: center;">🎾 ACEAPP TENNIS</h1>
                <h2 style="color: white;">Ciao {nome}!</h2>
                <p style="color: white; font-size: 16px;">
                    Benvenuto in ACEAPP — la prima piattaforma tennis con intelligenza artificiale biometrica!
                </p>
                <p style="color: white; font-size: 16px;">
                    Il nostro algoritmo ACEAI analizzerà il tuo profilo fisico e ti consiglierà 
                    l'attrezzatura perfetta per il tuo stile di gioco.
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://aceapp.it" style="background-color: #1A2E4C; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Scopri ACEAPP →
                    </a>
                </div>
                <p style="color: white; margin-top: 30px; font-size: 12px; text-align: center;">
                    © 2026 ACEAPP Tennis — info@aceapp.it
                </p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, BREVO_SMTP_KEY)
            server.sendmail(SMTP_USER, email, msg.as_string())

        print(f"Email benvenuto inviata a {email}")
        return True

    except Exception as e:
        print(f"Errore invio email: {e}")
        return False