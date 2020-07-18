from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from .database import Base


class Doctor(Base):
    """ SQLAlchemy model for `Doctor`. """

    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    appointments = relationship(
        'Appointment',
        back_populates='doctor',
        passive_deletes=True
    )


class Appointment(Base):
    """ SQLAlchemy model for `Appointment`. """

    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True)
    comment = Column(Text, nullable=True)
    start_dt = Column(DateTime, default=datetime.utcnow)
    end_dt = Column(DateTime)
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete='CASCADE'))

    doctor = relationship('Doctor', back_populates='appointments')
