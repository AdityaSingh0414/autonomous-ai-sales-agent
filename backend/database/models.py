
from sqlalchemy import Column, Integer, String
from backend.database.connection import Base


# Customer leads ka database model.
class Lead(Base):

    # Database table ka naam.
    __tablename__ = "leads"

    # Customer ki unique ID.
    id = Column(Integer, primary_key=True, index=True)

    # Customer details.
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    # Lead qualification details.
    score = Column(Integer)
    category = Column(String)


# Customer appointments ka database model.
class Appointment(Base):

    # Database table ka naam.
    __tablename__ = "appointments"

    # Appointment ki unique ID.
    id = Column(Integer, primary_key=True, index=True)

    # Customer details.
    customer_name = Column(String)
    email = Column(String)

    # Appointment scheduling details.
    appointment_date = Column(String)
    appointment_time = Column(String)

    # Default appointment status.
    status = Column(String, default="Scheduled")
