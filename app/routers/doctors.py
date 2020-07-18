from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.database import engine

# from app.main import get_db
# from ..models import models
# from ..models import schemas

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


@router.get('/', response_model=List[schemas.Doctor])
def fetch_doctors(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = crud.get_doctors(db, skip=skip, limit=limit)
    return doctors


@router.get('/{doctor_id}/', response_model=schemas.Doctor)
def fetch_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor(db=db, doctor_id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found.')
    return doctor


@router.post('/', response_model=schemas.Doctor)
def post_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    try:
        db_doctor = crud.create_doctor(db=db, doctor=doctor)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=404,
            detail='Doctor with this email is already registered.'
        )
    return db_doctor


@router.put('/{doctor_id}/', response_model=schemas.Doctor)
def put_doctor(
    doctor_id: int,
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db)
):
    doctor = crud.update_doctor(db=db, doctor=doctor, doctor_id=doctor_id)
    return doctor


@router.delete('/{doctor_id}/', status_code=204)
def destroy_doctor(doctor_id: int, db: Session = Depends(get_db)):
    crud.delete_doctor(db=db, doctor_id=doctor_id)
