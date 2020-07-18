from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import engine

# from ..main import get_db
from ..database import SessionLocal
from .. import crud
from .. import schemas
from .. import models


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', response_model=List[schemas.Appointment])
def fetch_appointments(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return appointments


@router.get('/{appointment_id}', response_model=schemas.Appointment)
def fetch_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail='Appointment not found.')
    return appointment


@router.post('/', response_model=schemas.Appointment)
def post_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):
    # breakpoint()
    # if appointment.start_dt > appointment.end_dt:
    #     raise HTTPException(
    #         status_code=404, detail='Start date is greater than end date.')

    db_appointment = crud.create_appointment(db, appointment)
    return db_appointment


@router.put('/{appointment_id}', response_model=schemas.Appointment)
def change_appointment(
    appointment: schemas.AppointmentCreate,
    appointment_id: int,
    db: Session = Depends(get_db)
):
    # if appointment.start_dt > appointment.end_dt:
    #     raise HTTPException(
    #         status_code=404, detail='Start date is greater than end date.')

    appointment = crud.update_appointment(db, appointment, appointment_id)
    return appointment


@router.delete('/{appointment_id}', status_code=204)
def destroy_appointment(appointment_id: int, db: Session = Depends(get_db)):
    crud.delete_appointment(db, appointment_id)
