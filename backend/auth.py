import os
import random

from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from . import crud

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")
ALGORITHM = "HS256"

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USER"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("SMTP_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)

def generar_otp():
    return str(random.randint(100000, 999999))


async def enviar_email_otp(email: str, otp: str):
    try:
        message = MessageSchema(
            subject="Código OTP",
            recipients=[email],
            body=f"Tu código OTP es: {otp}",
            subtype="plain"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        print("Error enviando correo:", e)
        raise HTTPException(status_code=500, detail="Error enviando correo")


async def enviar_otp(db, email):
    otp = generar_otp()

    crud.create_or_update_otp(db, email, otp)

    # 🔥 ENVÍA EMAIL REAL
    await enviar_email_otp(email, otp)

    return {"msg": "OTP enviado al correo"}


def verificar_otp(db, email, otp):
    user = crud.get_user_by_email(db, email)

    if user and user.otp == otp:
        token = crear_token(email)

        return {
            "msg": "Login exitoso",
            "token": token
        }

    raise HTTPException(status_code=400, detail="OTP incorrecto")


def crear_token(email: str):
    data = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]

    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")