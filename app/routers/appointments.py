from datetime import date
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.database import get_db


router = APIRouter()


@router.get('/', response_model=List[schemas.Appointment])
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Router to get a list of `Appointment` objects.

    Args:
    - **skip** (int, optional): Hints where to start during pagination.
        Defaults to 0.
    - **limit** (int, optional): Hints where to end during pagination.
        Defaults to 100.
    """
    db_appointments = crud.get_appointments(
        db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)
    return db_appointments


@router.get('/{appointment_id}/', response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Gets the `Appointment` object based with the designated appointment_id

    Args:
    - **appointment_id (int)**: PK of the object.
    """
    db_appointment = crud.get_appointment(db, appointment_id=appointment_id)
    return db_appointment


@router.post('/', response_model=schemas.Appointment)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create an `Appointment` with all the information in the request body.

    Args:
    - **patient_name (srt)**: Name of the patient.
    - **comment (str)**: Other comments for this appointment.
    - **start_dt (datetime)**: The start date and time of appointment.
    - **end_dt (datetime)**: The end date and time of appointment.
    - **doctor_id (int)**: The pk of the `Doctor` related to this specific
        appointment.
    """
    db_appointment = crud.create_appointment(db, appointment)
    return db_appointment


@router.put('/{appointment_id}/', response_model=schemas.Appointment)
def change_appointment(
    appointment: schemas.AppointmentCreate,
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """
    Update the `Appointment` object with all the information in the
    request body.

    Args:
    - **appointment_id (int)**: The pk of the appointment object.
    - **patient_name (str)**: Name of the patient.
    - **comment (str)**: Other comments for this appointment.
    - **start_dt (datetime)**: The start date and time of appointment.
    - **end_dt (datetime)**: The end date and time of appointment.
    - **doctor_id (int)**: The pk of the `Doctor` related to this specific
        appointment.
    """
    db_appointment = crud.update_appointment(db, appointment, appointment_id)
    return db_appointment


@router.delete('/{appointment_id}/', status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Deletes the `Appointment` object.

    Args:
    - **appointment_id (str)**: PK of the appointment object.
    """
    crud.delete_appointment(db, appointment_id)
