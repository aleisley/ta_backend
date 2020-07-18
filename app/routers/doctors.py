from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.database import get_db


router = APIRouter()


@router.get('/', response_model=List[schemas.Doctor])
def get_doctors(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Router to get a list of `Doctor` objects.

    Args:
    - **skip** (int, optional): Hints where to start during pagination.
        Defaults to 0.
    - **limit** (int, optional): Hints where to end during pagination.
        Defaults to 100.
    """
    db_doctors = crud.get_doctors(db, skip=skip, limit=limit)
    return db_doctors


@router.get('/{doctor_id}/', response_model=schemas.Doctor)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Gets the `Doctor` object based with the designated appointment_id

    Args:
    - **doctor_id (int)**: PK of the doctor object.
    """
    db_doctor = crud.get_doctor(db=db, doctor_id=doctor_id)
    return db_doctor


@router.get('/{doctor_id}/appointments/', response_model=schemas.Appointment)
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    """
    Gets all the `Appointment` objects related to this specific doctor.

    Args:
    - **doctor_id (int)**: PK of the doctor object.
    """
    pass


@router.post('/', response_model=schemas.Doctor)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """
    Create a `Doctor` with all the information in the request body.

    Args:
    - **first_name (str)**: First name of the doctor.
    - **last_name (str)**: Last name of the doctor.
    - **email (pydantic.EmailStr)**: Email address of the doctor.
    """
    db_doctor = crud.create_doctor(db, doctor)
    return db_doctor


@router.put('/{doctor_id}/', response_model=schemas.Doctor)
def change_doctor(
    doctor_id: int,
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db)
):
    """
    Update a `Doctor` with all the information in the request body.

    Args:
    - **doctor_id (str)**: PK of the doctor object.
    - **first_name (str)**: First name of the doctor.
    - **last_name (str)**: Last name of the doctor.
    - **email (pydantic.EmailStr)**: Email address of the doctor.
    """
    db_doctor = crud.update_doctor(db=db, doctor=doctor, doctor_id=doctor_id)
    return db_doctor


@router.delete('/{doctor_id}/', status_code=204)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Deletes the `Doctor` object.

    Args:
    - **doctor_id (str)**: PK of the doctor object.
    """
    crud.delete_doctor(db=db, doctor_id=doctor_id)
