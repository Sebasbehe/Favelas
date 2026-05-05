import os
import random

from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv

import resend

from . import crud


# Cargar variables de entorno
load_dotenv()


# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")
ALGORITHM = "HS256"


# Configurar Resend
resend.api_key = os.getenv("RESEND_API_KEY")


# Generar código OTP
def generar_otp():
    return str(random.randint(100000, 999999))


# Enviar OTP por correo
async def enviar_email_otp(email: str, otp: str):
    try:
        print("Enviando OTP a:", email)

        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [email],  # importante: como lista
            "subject": "Código de verificación",
            "html": f"""
                <h2>Tu código OTP</h2>
                <p>Tu código de verificación es:</p>
                <h1>{otp}</h1>
                <p>No compartas este código.</p>
            """
        })

        print("Respuesta de Resend:", response)

    except Exception as e:
        print("Error enviando correo:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error enviando correo: {str(e)}"
        )


# Generar y guardar OTP
async def enviar_otp(db, email):
    otp = generar_otp()

    # Guardar en base de datos
    crud.create_or_update_otp(db, email, otp)

    # Enviar correo
    await enviar_email_otp(email, otp)

    return {
        "msg": "OTP enviado al correo"
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


# Crear JWT
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


# Verificar JWT
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