from datetime import datetime

from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class AppointmentBase(BaseModel):
    """ Base schema for `Appointment` objects. """

    patient_name: str
    comment: Optional[str] = None
    start_dt: datetime
    end_dt: datetime
    doctor_id: int


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
