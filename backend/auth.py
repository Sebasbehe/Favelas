import os
import random
import smtplib

from email.mime.text import MIMEText
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv

from . import crud


# Cargar variables de entorno
load_dotenv()


# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")
ALGORITHM = "HS256"


# Credenciales de Gmail
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Generar código OTP
def generar_otp():
    return str(random.randint(100000, 999999))


# Enviar OTP por correo
async def enviar_email_otp(email: str, otp: str):
    try:
        print("Enviando OTP a:", email)

        html = f"""
        <h2>Tu código de verificación</h2>
        <p>Tu código OTP es:</p>
        <h1>{otp}</h1>
        <p>No compartas este código.</p>
        """

        msg = MIMEText(html, "html")
        msg["Subject"] = "Código de verificación"
        msg["From"] = EMAIL_USER
        msg["To"] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            server.login(
                EMAIL_USER,
                EMAIL_PASSWORD
            )

            server.send_message(msg)

        print("Correo enviado correctamente")

    except Exception as e:
        print("Error SMTP:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error enviando correo: {str(e)}"
        )


# Generar y guardar OTP
async def enviar_otp(db, email):
    otp = generar_otp()

    # Guardar OTP en la base de datos
    crud.create_or_update_otp(db, email, otp)

    # Enviar OTP al correo
    await enviar_email_otp(email, otp)

    return {
        "msg": "OTP enviado correctamente"
    }


# Verificar OTP
def verificar_otp(db, email, otp):
    user = crud.get_user_by_email(db, email)

    if user and user.otp == otp:
        token = crear_token(email)

        return {
            "msg": "Login exitoso",
            "token": token
        }

    raise HTTPException(
        status_code=400,
        detail="OTP incorrecto"
    )


# Crear token JWT
def crear_token(email: str):
    data = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Verificar token JWT
def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["sub"]

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )