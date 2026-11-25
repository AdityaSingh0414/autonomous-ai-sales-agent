from fastapi import APIRouter
from backend.database.connection import SessionLocal
from backend.database.models import Lead, Appointment

router = APIRouter()


@router.get("/analytics")
def get_analytics():

    db = SessionLocal()

    try:
        total_leads = db.query(Lead).count()
        total_appointments = db.query(Appointment).count()

        hot_leads = db.query(Lead).filter(
            Lead.category == "Hot"
        ).count()

        return {
            "total_leads": total_leads,
            "hot_leads": hot_leads,
            "total_appointments": total_appointments
        }

    finally:
        db.close()