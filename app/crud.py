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


def update_doctor(db: Session, doctor: schemas.DoctorCreate, doctor_id: int):
    db_doctor = get_doctor(db, doctor_id)
    for key, value in doctor:
        setattr(db_doctor, key, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: int):
    db_doctor = get_doctor(db, doctor_id)
    db.delete(db_doctor)
    db.commit()


def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).get(appointment_id)


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()


def create_appointment(db: Session, appointment: schemas.Appointment):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def update_appointment(
    db: Session,
    appointment: schemas.Appointment,
    appointment_id: int
):
    db_appointment = get_appointment(db, appointment_id)
    for key, value in appointment:
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    db_appointment = get_doctor(db, appointment_id)
    db.delete(db_appointment)
    db.commit()
