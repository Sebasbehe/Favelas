import random
import os

from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv

from . import crud

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")
ALGORITHM = "HS256"

# -------------------------
# 🔐 OTP GENERATOR
# -------------------------
def generar_otp():
    return str(random.randint(100000, 999999))


# -------------------------
# 📤 ENVIAR OTP (CORREGIDO)
# -------------------------
def enviar_otp(db, email):
    otp = generar_otp()

    # guardar OTP en la base de datos
    crud.create_or_update_otp(db, email, otp)

    # 🔥 IMPORTANTE: solo logs (evita error 500 en Render)
    print(f"OTP generado para {email}: {otp}")

    return {
        "msg": "OTP generado correctamente"
    }


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

    raise HTTPException(status_code=400, detail="OTP incorrecto")


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

    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")