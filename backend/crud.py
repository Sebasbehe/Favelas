from sqlalchemy.orm import Session
from . import models, schemas

def crear_estudiante(db: Session, estudiante: schemas.EstudianteCreate, email: str):
    nuevo = models.Estudiante(
        nombre=estudiante.nombre,
        edad=estudiante.edad,
        nota=estudiante.nota,
        owner=email
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def obtener_estudiantes(db: Session, email: str):
    return db.query(models.Estudiante).filter(models.Estudiante.owner == email).all()


def obtener_estudiante(db: Session, estudiante_id: int):
    return db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()


def actualizar_estudiante(db: Session, estudiante_id: int, datos: schemas.EstudianteCreate, email: str):
    estudiante = db.query(models.Estudiante).filter(
        models.Estudiante.id == estudiante_id,
        models.Estudiante.owner == email
    ).first()

    if estudiante:
        estudiante.nombre = datos.nombre
        estudiante.edad = datos.edad
        estudiante.nota = datos.nota
        db.commit()
        db.refresh(estudiante)

    return estudiante


def eliminar_estudiante(db: Session, estudiante_id: int, email: str):
    estudiante = db.query(models.Estudiante).filter(
        models.Estudiante.id == estudiante_id,
        models.Estudiante.owner == email
    ).first()

    if estudiante:
        db.delete(estudiante)
        db.commit()

    return estudiante


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_or_update_otp(db: Session, email: str, otp: str):
    user = get_user_by_email(db, email)

    if user:
        user.otp = otp
    else:
        user = models.User(email=email, otp=otp)
        db.add(user)

    db.commit()
    db.refresh(user)
    return user