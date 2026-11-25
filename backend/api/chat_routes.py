
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.agents.llm import generate_response
from backend.intelligence.lead_qualification import qualify_lead
from backend.intelligence.sentiment_analysis import analyze_sentiment
from backend.database.connection import SessionLocal
from backend.database.models import Lead


# API router create karna.
router = APIRouter()


# Chat request ka data structure.
class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] = Field(default_factory=list)


# Customer chat endpoint.
@router.post("/chat")
def chat(request: ChatRequest):

    try:
        # Previous conversation ke saath current message add karna.
        messages = request.history + [
            {
                "role": "user",
                "content": request.message
            }
        ]

        # LLM se AI response generate karna.
        reply = generate_response(messages)

        # Customer ki lead qualification karna.
        lead = qualify_lead(request.message)

        # Customer ke message ka sentiment analyze karna.
        sentiment = analyze_sentiment(request.message)

        db = SessionLocal()
        try:
            db.add(Lead(
                name=None,
                email=None,
                phone=None,
                score=lead["score"],
                category=lead["category"]
            ))
            db.commit()
        finally:
            db.close()

        # Complete result frontend ko return karna.
        return {
            "reply": reply,
            "lead_score": lead["score"],
            "lead_category": lead["category"],
            "lead_details": lead["details"],
            "sentiment": sentiment
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
