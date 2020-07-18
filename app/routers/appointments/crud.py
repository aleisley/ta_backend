from sqlalchemy.orm import Session

from app import models
from app import schemas


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
