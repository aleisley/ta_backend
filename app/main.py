from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers.appointments import router as appointment_router
from .routers.doctors import router as doctor_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(
    appointment_router,
    prefix='/appointments',
    tags=['appointments'],
    responses={404: {'description': 'Not Found'}}
)

app.include_router(
    doctor_router,
    prefix='/doctors',
    tags=['doctors'],
    responses={404: {'description': 'Not Found'}}
)
