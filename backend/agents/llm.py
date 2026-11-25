
import os

from dotenv import load_dotenv
from groq import Groq

from backend.agents.prompts import SYSTEM_PROMPT
from backend.rag.retriever import retrieve_context


# Environment variables load karna.
load_dotenv()


# Groq client initialize karna.
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None


# LLM model select karna.
MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# AI response generate karne ka function.
def generate_response(messages):
    if client is None:
        question = messages[-1]["content"]
        return (
            "The chat service is ready, but GROQ_API_KEY is not configured. "
            f"I received your message: {question}"
        )

    # Latest customer question nikalna.
    question = messages[-1]["content"]

    # RAG retriever se relevant company information lena.
    context = retrieve_context(question)

    # System prompt ke saath company context add karna.
    conversation = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + "\n\nUse the following company information:\n"
                + context
                + "\nOnly use this information for company-specific facts."
            )
        }
    ]

    # Previous conversation history add karna.
    conversation.extend(messages)

    # Groq API se AI response generate karna.
    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation,
        max_completion_tokens=500
    )

    # Generated AI response return karna.
    return response.choices[0].message.content
