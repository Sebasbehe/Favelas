from fastapi import FastAPI, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.email_utils import enviar_correo

from . import crud, schemas, auth, models
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://favelas.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# MODELO PARA CORREOS
# =========================

class EmailRequest(BaseModel):
    destinatario: str
    asunto: str
    mensaje: str


# =========================
# ENDPOINT ENVIAR CORREO
# =========================

@app.post("/send-email")
def send_email(data: EmailRequest):

    return enviar_correo(
        data.destinatario,
        data.asunto,
        data.mensaje
    )


# =========================
# AUTENTICACION
# =========================

@app.post("/auth/send-otp")
async def send_otp(data: schemas.EmailSchema, db: Session = Depends(get_db)):
    return await auth.enviar_otp(db, data.email)


@app.post("/auth/verify-otp")
def verify_otp(data: schemas.OTPVerify, db: Session = Depends(get_db)):
    return auth.verificar_otp(db, data.email, data.otp)


# =========================
# CRUD ESTUDIANTES
# =========================

@app.post("/students")
def crear(est: schemas.EstudianteCreate, token: str = Header(...), db: Session = Depends(get_db)):
    email = auth.verificar_token(token)
    return crud.crear_estudiante(db, est, email)


@app.get("/students")
def listar(token: str = Header(...), db: Session = Depends(get_db)):
    email = auth.verificar_token(token)
    return crud.obtener_estudiantes(db, email)


@app.get("/students/{id}")
def obtener(id: int, token: str = Header(...), db: Session = Depends(get_db)):
    email = auth.verificar_token(token)
    return crud.obtener_estudiante(db, id)


@app.put("/students/{id}")
def actualizar(id: int, datos: schemas.EstudianteCreate, token: str = Header(...), db: Session = Depends(get_db)):
    email = auth.verificar_token(token)
    return crud.actualizar_estudiante(db, id, datos, email)


@app.delete("/students/{id}")
def eliminar(id: int, token: str = Header(...), db: Session = Depends(get_db)):
    email = auth.verificar_token(token)
    return crud.eliminar_estudiante(db, id, email)