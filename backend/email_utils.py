import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def enviar_correo(destinatario: str, asunto: str, mensaje: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = destinatario
        msg["Subject"] = asunto

        msg.attach(MIMEText(mensaje, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_USER, EMAIL_PASSWORD)
            servidor.sendmail(
                EMAIL_USER,
                destinatario,
                msg.as_string()
            )

        return {
            "success": True,
            "message": f"Correo enviado a {destinatario}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }