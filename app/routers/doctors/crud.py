from sqlalchemy.orm import Session

from app import models
from app import schemas


def get_doctor(db: Session, doctor_id: int):
    # return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    return db.query(models.Doctor).get(doctor_id)


def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Doctor).offset(skip).limit(limit).all()


def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
