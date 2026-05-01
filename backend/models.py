from sqlalchemy import Column, Integer, String
from .database import Base

# Usuario para autenticación OTP
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    otp = Column(String)

# Estudiantes
class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)  # 🔥 clave
    nombre = Column(String)
    edad = Column(Integer)
    nota = Column(Integer)