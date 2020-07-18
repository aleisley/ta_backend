import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app import schemas


logger = logging.getLogger(__name__)


def get_doctor(db: Session, doctor_id: int):
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
    """
    Return an appointment instance

    Args:
        appointment_id (int): pk of the appointment

    Raises:
        HTTPException: Raises 404 if no appointment object with the
            given appointment_id is found.

    Returns:
        Appointment: the appointment instance
    """
    db_appointment = db.query(models.Appointment).get(appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail='Appointment not found.')
    return db_appointment


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    """
    Returns a queryset of appointments.

    Args:
        skip (int, optional): Start of pagination. Defaults to 0.
        limit (int, optional): End of pagination. Defaults to 100.

    Returns:
        List[Appointment]: A list of Appointment objects
    """
    return db.query(models.Appointment).offset(skip).limit(limit).all()


def create_appointment(db: Session, appointment: schemas.Appointment):
    """
    Creates the object based on the given appointment schema.

    Args:
        appointment (schemas.Appointment): Comes from the body of the
            POST request.

    Raises:
        HTTPException: Raises 422 if there are overlapping (overbooked)
            appointment times.

    Returns:
        Appointment: An appointment instance.
    """
    db_doctor = get_doctor(db, appointment.doctor_id)
    for app in db_doctor.appointments:
        if (
            app.end_dt >= appointment.start_dt and
            app.start_dt <= appointment.end_dt
        ):
            raise HTTPException(
                status_code=422,
                detail='Overlapping appointment times.'
            )

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
    if db_appointment.doctor_id != appointment.doctor_id:
        db_doctor = get_doctor(db, appointment.doctor_id)
        logger.info(
            f'The appointment doctor id will change from '
            f'{db_appointment.doctor_id} to {db_doctor.id}.'
        )
    else:
        db_doctor = get_doctor(db, db_appointment.doctor_id)
        logger.info(f'The appointment doctor id is unchanged.')

    for app in db_doctor.appointments:
        if app.id == db_appointment.id:
            continue
        if (
            app.end_dt >= appointment.start_dt and
            app.start_dt <= appointment.end_dt
        ):
            raise HTTPException(
                status_code=422,
                detail='Overlapping appointment times.'
            )

    for key, value in appointment:
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    db_appointment = get_doctor(db, appointment_id)
    db.delete(db_appointment)
    db.commit()
