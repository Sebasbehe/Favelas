from pydantic import BaseModel



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



class EmailSchema(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str