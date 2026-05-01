from fastapi import FastAPI, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, schemas, auth
import models
from database import engine
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# 🧠 DB
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# 🔐 AUTH OTP
# -----------------------
@app.post("/auth/send-otp")
def send_otp(data: schemas.EmailSchema, db: Session = Depends(get_db)):
    return auth.enviar_otp(db, data.email)

@app.post("/auth/verify-otp")
def verify_otp(data: schemas.OTPVerify, db: Session = Depends(get_db)):
    return auth.verificar_otp(db, data.email, data.otp)

# -----------------------
# 📚 CRUD ESTUDIANTES
# -----------------------

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