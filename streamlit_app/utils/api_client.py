
# requests library import kar rahe hain.
# Iska use backend API ko request bhejne ke liye hota hai.
import requests


# FastAPI backend ka URL.
API_URL = "http://127.0.0.1:8000"


# Ye function user ka message backend ko send karega.
def send_message(message: str, history: list[dict[str, str]] | None = None):

    try:
        # Backend ke /api/chat endpoint par POST request bhej rahe hain.
        response = requests.post(
            f"{API_URL}/api/chat",

            # Message JSON format mein send kar rahe hain.
            json={
                "message": message,
                "history": history or []
            },

            # Maximum 30 seconds wait karega.
            timeout=30
        )

        # Agar API mein error hai toh exception raise karega.
        response.raise_for_status()

        # JSON response se reply extract karke return karega.
        return response.json()["reply"]


    # Agar backend start nahi hai toh ye error show hoga.
    except requests.exceptions.ConnectionError:
        return "Error: Backend is not running. Please start FastAPI."


    # Kisi aur API-related error ko handle karega.
    except requests.exceptions.RequestException as error:
        return f"API Error: {error}"
