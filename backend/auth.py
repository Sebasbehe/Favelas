import random
import smtplib
import os

from jose import jwt
from datetime import datetime, timedelta
from email.message import EmailMessage
from fastapi import HTTPException
from dotenv import load_dotenv

from . import crud   # 🔥 CORREGIDO

load_dotenv()

SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


# -------------------------
# 🔐 OTP GENERATOR
# -------------------------
def generar_otp():
    return str(random.randint(100000, 999999))


# -------------------------
# 📧 ENVIAR EMAIL OTP
# -------------------------
def enviar_email_otp(email: str, otp: str):

    msg = EmailMessage()
    msg["Subject"] = "Tu código OTP"
    msg["From"] = SMTP_USER
    msg["To"] = email
    msg.set_content(f"Tu código OTP es: {otp}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)

    except Exception as e:
        print("Error enviando OTP:", e)
        raise HTTPException(status_code=500, detail="Error enviando correo")


# -------------------------
# 📤 ENVIAR OTP
# -------------------------
def enviar_otp(db, email):
    otp = generar_otp()

    crud.create_or_update_otp(db, email, otp)

    enviar_email_otp(email, otp)

    return {"msg": "OTP enviado al correo"}


# -------------------------
# 🔍 VERIFICAR OTP
# -------------------------
def verificar_otp(db, email, otp):

    user = crud.get_user_by_email(db, email)

    if user and user.otp == otp:
        token = crear_token(email)

        return {
            "msg": "Login exitoso",
            "token": token
        }

    return {"error": "OTP incorrecto"}


# -------------------------
# 🔑 JWT TOKEN
# -------------------------
def crear_token(email: str):
    data = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------
# 🧠 VALIDAR TOKEN
# -------------------------
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]

    except:
        raise HTTPException(status_code=401, detail="Token inválido")