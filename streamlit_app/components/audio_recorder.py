# Microphone recording component import kar rahe hain.
from streamlit_mic_recorder import mic_recorder


# Audio recording function.
def record_audio():

    # User ko Start aur Stop Recording buttons show honge.
    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        format="webm",
        key="sales_voice"
    )

    # Recorded audio return kar rahe hain.
    return audio