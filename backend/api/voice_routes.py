
from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from backend.voice.speech_to_text import transcribe_audio
from backend.voice.text_to_speech import generate_audio
from backend.agents.llm import generate_response


# API router create kar rahe hain.
router = APIRouter()
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
RESPONSE_AUDIO_PATH = DATA_DIR / "response.mp3"
AUDIO_EXTENSIONS = {
    "audio/webm": ".webm",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/mpeg": ".mp3"
}


# Customer voice upload aur AI response generate karne ka endpoint.
@router.post("/voice")
async def voice_chat(audio: UploadFile = File(...)):
    try:
        content_type = (audio.content_type or "").split(";", 1)[0].lower()
        extension = AUDIO_EXTENSIONS.get(content_type)
        if extension is None:
            raise HTTPException(
                status_code=415,
                detail="Unsupported audio format. Upload WebM, WAV, or MP3 audio."
            )

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        audio_path = DATA_DIR / f"input_audio{extension}"

        # Uploaded audio ko local file mein save karna.
        with audio_path.open("wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # Audio ko text mein convert karna (Speech-to-Text).
        transcription = transcribe_audio(str(audio_path))

        # Transcription dictionary se text aur language nikalna.
        user_text = transcription["text"]
        detected_language = transcription["language"]

        # Check karna ki speech detect hui hai ya nahi.
        if not user_text:
            raise HTTPException(
                status_code=400,
                detail="No speech detected"
            )

        # Customer ke message se AI response generate karna.
        reply = generate_response([
            {
                "role": "user",
                "content": user_text
            }
        ])

        # AI response ko audio mein convert karna (Text-to-Speech).
        generate_audio(
            reply,
            output_path=str(RESPONSE_AUDIO_PATH),
            language=detected_language
        )

        # Customer text, detected language aur AI response return karna.
        return {
            "user_text": user_text,
            "detected_language": detected_language,
            "reply": reply,
            "audio_url": "/api/voice/audio"
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        # Uploaded audio file close karna.
        await audio.close()


# Generated MP3 audio play/download karne ka endpoint.
@router.get("/voice/audio")
def get_audio():
    # Check karna ki generated audio available hai ya nahi.
    if not RESPONSE_AUDIO_PATH.is_file() or RESPONSE_AUDIO_PATH.stat().st_size == 0:
        raise HTTPException(
            status_code=404,
            detail="Audio file not found"
        )

    # MP3 audio file frontend ko return karna.
    return FileResponse(
        path=RESPONSE_AUDIO_PATH,
        media_type="audio/mpeg",
        filename="response.mp3"
    )