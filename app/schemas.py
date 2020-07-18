from datetime import datetime

from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

from . import constants


class AppointmentBase(BaseModel):
    """ Base schema for `Appointment` objects. """

    patient_name: str
    comment: Optional[str] = None
    start_dt: datetime
    end_dt: datetime
    doctor_id: int

    @validator('end_dt')
    def validate_datetimes(cls, dt, values):

        # return immediately since format of start date is probably wrong.
        if 'start_dt' not in values:
            return dt

        if values['start_dt'].weekday() != dt.weekday():
            raise ValueError('Appointment not within the same date.')

        if dt.weekday() == constants.NO_APPOINTMENT_WEEKDAY_CODE:
            raise ValueError('Appointments not available on Sundays.')

        if values['start_dt'] > dt:
            raise ValueError('End time should be greater than start time.')

        # create start and end datetime for comparisons
        start_of_day = dt.replace(hour=9, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day.replace(hour=17)

        if not start_of_day <= values['start_dt'] <= end_of_day:
            raise ValueError('Start time should be within permissible hours.')

        if not start_of_day <= dt <= end_of_day:
            raise ValueError('End time should be within permissible hours.')

        return dt


class Appointment(AppointmentBase):
    """ Schema used for `Appointment` GET requests. """

    id: int

    class Config:
        orm_mode = True


class AppointmentCreate(AppointmentBase):
    """ Schema used for `Appointment` POST or PUT requests. """

    pass


class DoctorBase(BaseModel):
    """ Base schema for `Doctor` objects. """

    first_name: str
    last_name: str
    email: EmailStr


class Doctor(DoctorBase):
    """ Schema used for `Doctor` GET requests. """

    id: int
    appointments: List[Appointment] = []

    class Config:
        orm_mode = True


class DoctorCreate(DoctorBase):
    """ Schema used for `DOCTOR` GET or PUT requests. """

    pass
