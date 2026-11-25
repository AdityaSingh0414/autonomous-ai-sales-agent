
from gtts import gTTS


# Supported languages.
LANGUAGE_MAP = {
    "en": "en",
    "hi": "hi"
}


def generate_audio(
    text,
    output_path="data/response.mp3",
    language="en"
):

    # Detected language ke according TTS language select karna.
    language = LANGUAGE_MAP.get(language, "en")

    # AI response ko speech mein convert karna.
    speech = gTTS(
        text=text,
        lang=language
    )

    # Generated speech ko MP3 file mein save karna.
    speech.save(output_path)

    # Generated audio ka path return karna.
    return output_path
