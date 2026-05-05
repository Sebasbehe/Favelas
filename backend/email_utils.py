import os
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")


def enviar_correo(destinatario, asunto, mensaje):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "Favelas",
            "email": "epsistemas@e2energiaeficiente.com"
        },
        "to": [
            {
                "email": destinatario
            }
        ],
        "subject": asunto,
        "htmlContent": mensaje
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    return response.json()