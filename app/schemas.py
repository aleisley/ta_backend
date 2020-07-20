from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

from .utils import NO_APPOINTMENT_WEEKDAY_CODE
from .utils import utc_to_local


class DoctorBase(BaseModel):
    """ Base schema for `Doctor` objects. """

    first_name: str
    last_name: str
    email: EmailStr


class Doctor(DoctorBase):
    """ Schema used for `Doctor` GET requests. """

    id: int
    # appointments: List[Appointment] = []

    class Config:
        orm_mode = True


class DoctorCreate(DoctorBase):
    """ Schema used for `DOCTOR` GET or PUT requests. """

    pass


class AppointmentBase(BaseModel):
    """ Base schema for `Appointment` objects. """

    patient_name: str
    comment: Optional[str] = None
    start_dt: datetime
    end_dt: datetime
    # doctor_id: int

    @validator('end_dt')
    def validate_datetimes(cls, dt, values):

        # return immediately since format of start date is probably wrong.
        if 'start_dt' not in values:
            return dt

        # Convert to aware timezones.
        aware_start_dt = utc_to_local(values['start_dt'])
        aware_end_dt = utc_to_local(dt)

        print(aware_start_dt)

        if aware_start_dt.weekday() != aware_end_dt.weekday():
            raise HTTPException(
                status_code=422,
                detail='Appointment not within the same date.'
            )

        if aware_end_dt.weekday() == NO_APPOINTMENT_WEEKDAY_CODE:
            raise HTTPException(
                status_code=422,
                detail='Appointments not available on Sundays.'
            )

        if aware_start_dt > aware_end_dt:
            raise HTTPException(
                status_code=422,
                detail='End time should be greater than start time.'
            )

        # create start and end datetime for comparisons
        start_of_day = aware_end_dt.replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0,
        )
        end_of_day = start_of_day.replace(hour=17)

        if not start_of_day <= aware_start_dt <= end_of_day:
            raise HTTPException(
                status_code=422,
                detail='Start time should be within permissible hours.'
            )

        if not start_of_day <= aware_end_dt <= end_of_day:
            raise HTTPException(
                status_code=422,
                detail='End time should be within permissible hours.'
            )

        # Return the naive timezone
        return dt


class Appointment(AppointmentBase):
    """ Schema used for `Appointment` GET requests. """

    id: int
    doctor_id: int
    doctor: Doctor

    class Config:
        orm_mode = True


class AppointmentCreate(AppointmentBase):
    """ Schema used for `Appointment` POST or PUT requests. """

    doctor_id: int


class AppointmentWithoutDoctorCreate(AppointmentBase):
    """
    Schema used for `Appointment` POST requests without the need
    for a doctor id.
    """

    pass

