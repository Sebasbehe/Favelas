from pydantic import BaseModel

# -----------------------
# 📚 ESTUDIANTES
# -----------------------

class EstudianteBase(BaseModel):
    nombre: str
    edad: int
    nota: int

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteResponse(EstudianteBase):
    id: int

    class Config:
        from_attributes = True

# -----------------------
# 🔐 AUTH
# -----------------------

class EmailSchema(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str