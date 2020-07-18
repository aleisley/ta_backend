from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.database import get_db


router = APIRouter()


@router.get('/', response_model=List[schemas.Appointment])
def get_appointments(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return appointments


@router.get('/{appointment_id}/', response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail='Appointment not found.')
    return appointment


@router.post('/', response_model=schemas.Appointment)
def post_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):
    db_appointment = crud.create_appointment(db, appointment)
    return db_appointment


@router.put('/{appointment_id}/', response_model=schemas.Appointment)
def change_appointment(
    appointment: schemas.AppointmentCreate,
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = crud.update_appointment(db, appointment, appointment_id)
    return appointment


@router.delete('/{appointment_id}/', status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    crud.delete_appointment(db, appointment_id)
