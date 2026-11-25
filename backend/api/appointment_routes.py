
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database.connection import SessionLocal
from backend.database.models import Appointment


# Appointment API router create karna.
router = APIRouter()


# Appointment request ka data structure.
class AppointmentRequest(BaseModel):

    customer_name: str
    email: str
    appointment_date: str
    appointment_time: str


# New appointment book karne ka endpoint.
@router.post("/appointments")
def create_appointment(request: AppointmentRequest):

    # Database session create karna.
    db = SessionLocal()

    try:
        # Appointment object create karna.
        appointment = Appointment(
            customer_name=request.customer_name,
            email=request.email,
            appointment_date=request.appointment_date,
            appointment_time=request.appointment_time
        )

        # Appointment database mein add karna.
        db.add(appointment)

        # Database changes save karna.
        db.commit()

        # Newly created appointment ki ID refresh karna.
        db.refresh(appointment)

        # Booking confirmation return karna.
        return {
            "message": "Appointment booked successfully!",
            "appointment_id": appointment.id
        }

    except Exception as error:

        # Error aane par database changes rollback karna.
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        # Database connection close karna.
        db.close()
