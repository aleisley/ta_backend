import logging
from datetime import date
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import models
from app import schemas


logger = logging.getLogger(__name__)


def get_doctor(db: Session, doctor_id: int):
    """
    Return a `Doctor` object.

    Args:
        doctor_id (int): PK of the doctor object.

    Raises:
        HTTPException: Raises 404 if no doctor object is found with
            the given doctor_id.

    Returns:
        Doctor: A Doctor instance with the Doctor schema.
    """
    db_doctor = db.query(models.Doctor).get(doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail='Doctor not found.')
    return db_doctor


def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    """
    Return a list of `Doctor` objects.

    Args:
        skip (int, optional): Start of pagination. Defaults to 0.
        limit (int, optional): End of pagination. Defaults to 100.

    Returns:
        List[Doctor]: Returns a list of Doctor objects with the Doctor schema
    """
    return db.query(models.Doctor).offset(skip).limit(limit).all()


def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    """
    Creates a `Doctor` object given a DoctorCreate schema.

    Args:
        doctor (schemas.DoctorCreate): Schema to follow during
            creation. Also holds details for creation.

    Raises:
        HTTPException: Raises 422 when user will break the unique
            constraint of the email.

    Returns:
        Doctor: A `Doctor` object following the Doctor schema.
    """
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)

    try:
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code=422,
            detail='Doctor with this email is already registered.'
        )

    db.refresh(db_doctor)
    return db_doctor


def update_doctor(db: Session, doctor: schemas.DoctorCreate, doctor_id: int):
    """
    Updates a `Doctor` object given a DoctorCreate schema.

    Args:
        doctor (schemas.DoctorCreate): Schema to follow during update.
            Also holds details for the update.
        doctor_id (int): PK of the object to update.

    Raises:
        HTTPException: Raises 422 when user will break the unique
            constraint of the email.

    Returns:
        Doctor: A `Doctor` object following the Doctor schema.
    """
    db_doctor = get_doctor(db, doctor_id)
    for key, value in doctor:
        setattr(db_doctor, key, value)

    try:
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code=422,
            detail='Doctor with this email is already registered.'
        )

    db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: int):
    """
    Deletes a `Doctor` object.

    Args:
        doctor_id (int): Pk of the Doctor object to be deleted.
    """
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


def get_appointments(
    db: Session,
    start_date: date,
    end_date: date,
    skip: int = 0,
    limit: int = 100
):
    """
    Returns a queryset of appointments.

    Args:
        skip (int, optional): Start of pagination. Defaults to 0.
        limit (int, optional): End of pagination. Defaults to 100.

    Returns:
        List[Appointment]: A list of Appointment objects
    """
    db_appointments = db.query(models.Appointment)
    if start_date:
        start_dt = datetime(start_date.year, start_date.month, start_date.day)
        db_appointments = db_appointments.filter(
            models.Appointment.start_dt >= start_dt)
    if end_date:
        end_dt = datetime(end_date.year, end_date.month, end_date.day)
        db_appointments = db_appointments.filter(
            models.Appointment.end_dt <= end_dt)
    return db_appointments.offset(skip).limit(limit).all()


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
            app.end_dt > appointment.start_dt and
            app.start_dt < appointment.end_dt
        ):
            raise HTTPException(
                status_code=422,
                detail='Overlapping appointment times.'
            )

    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    logger.info(
        f'Appointment with id #{db_appointment.id} successfully created'
    )
    return db_appointment


def update_appointment(
    db: Session,
    appointment: schemas.Appointment,
    appointment_id: int
):
    """
    Updates the object based on the given appointment schema.

    Args:
        appointment (schemas.Appointment): Comes from the body of the
            POST request.
        appointment_id (int): PK of the appointment object.

    Raises:
        HTTPException: Raises 422 if there are overlapping (overbooked)
            appointment times.

    Returns:
        Appointment: An appointment instance.
    """
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
            app.end_dt > appointment.start_dt and
            app.start_dt < appointment.end_dt
        ):
            raise HTTPException(
                status_code=422,
                detail='Overlapping appointment times.'
            )

    for key, value in appointment:
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    logger.info(
        f'Appointment object with id #{db_appointment.id} successfully updated'
    )
    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    """
    Deletes an appointment object.

    Args:
        appointment_id (int): The PK of the appointment object.
    """
    db_appointment = get_doctor(db, appointment_id)
    db.delete(db_appointment)
    db.commit()
