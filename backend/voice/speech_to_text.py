
# Faster Whisper import kar rahe hain.
try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None


model = None


def _get_model():
    global model
    if model is None:
        if WhisperModel is None:
            raise RuntimeError("faster-whisper is not installed")
        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )
    return model


# Audio ko text mein convert karne ka function.
def transcribe_audio(audio_path):
    whisper_model = _get_model()

    # Audio transcribe karna aur language detect karna.
    segments, info = whisper_model.transcribe(
        audio_path,
        task="transcribe"
    )

    # Saare segments ko ek text mein combine karna.
    text = " ".join(
        segment.text for segment in segments
    )

    # Text aur detected language return karna.
    return {
        "text": text.strip(),
        "language": info.language
    }
