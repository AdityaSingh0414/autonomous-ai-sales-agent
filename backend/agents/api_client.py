
import requests

API_URL = "http://127.0.0.1:8000"


# Ab function 2 parameters accept karega.
def send_message(message: str, history: list):

    try:
        response = requests.post(
            f"{API_URL}/api/chat",

            # Message aur previous chat history backend ko bhejenge.
            json={
                "message": message,
                "history": history
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()["reply"]

    except requests.exceptions.ConnectionError:
        return "Error: Backend is not running. Please start FastAPI."

    except requests.exceptions.RequestException as error:
        return f"API Error: {error}"
