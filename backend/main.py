
# FastAPI application create karne ke liye.
from fastapi import FastAPI

# API routers import karna.
from backend.api.chat_routes import router as chat_router
from backend.api.voice_routes import router as voice_router
from backend.api.appointment_routes import router as appointment_router
from backend.api.analytics_routes import router as analytics_router
from backend.database.connection import Base, engine
from backend.database import models  # noqa: F401


# Main FastAPI application.
app = FastAPI(
    title="Autonomous AI Sales Agent",
    description="AI-powered sales assistant API",
    version="1.0.0"
)


@app.on_event("startup")
def initialize_database():
    Base.metadata.create_all(bind=engine)


# Home API.
@app.get("/")
def home():
    return {
        "message": "Autonomous AI Sales Agent API is running!"
    }


# Health check API.
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Chat API: /api/chat
app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"]
)


# Voice API: /api/voice
app.include_router(
    voice_router,
    prefix="/api",
    tags=["Voice"]
)


# Appointment API: /api/appointments
app.include_router(
    appointment_router,
    prefix="/api",
    tags=["Appointments"]
)

app.include_router(
    analytics_router,
    prefix="/api",
    tags=["Analytics"]
)
