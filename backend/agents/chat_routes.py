
# FastAPI se APIRouter aur HTTPException import kar rahe hain.
from fastapi import APIRouter, HTTPException

# BaseModel request data validate karne ke liye use hota hai.
from pydantic import BaseModel

# LLM file se AI response generate karne wala function import kar rahe hain.
from backend.agents.llm import generate_response


# API router create kar rahe hain.
router = APIRouter()


# User request ka structure define kar rahe hain.
class ChatRequest(BaseModel):
    message: str  # Current user message
    history: list[dict[str, str]] = []  # Previous conversation history


# Chat API endpoint create kar rahe hain.
@router.post("/chat")
def chat(request: ChatRequest):

    try:
        # Previous chat history ke saath current message add kar rahe hain.
        messages = request.history + [
            {
                "role": "user",
                "content": request.message
            }
        ]

        # LLM ko messages bhejkar AI response generate kar rahe hain.
        reply = generate_response(messages)

        # AI ka reply JSON format mein return kar rahe hain.
        return {"reply": reply}

    # Agar processing mein koi error aaye toh usko handle karenge.
    except Exception as error:
        raise HTTPException(
            status_code=500,  # Internal Server Error
            detail=str(error)  # Error ki details
        )
