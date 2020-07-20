from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import engine
from .models import Base
from .routers.appointments import router as appointment_router
from .routers.doctors import router as doctor_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['http://localhost', 'http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


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
