
# Streamlit UI aur API request ke liye imports.
import streamlit as st
import requests

# Microphone recording function import kar rahe hain.
from components.audio_recorder import record_audio
from utils.audio import to_wav_bytes


# Application title.
st.title("🎙️ AI Voice Sales Agent")

# FastAPI backend URL.
API_URL = "http://127.0.0.1:8000"


# Microphone se audio record karna.
audio = record_audio()


# Check karna ki audio record hui hai ya nahi.
if audio:

    # Recorded audio ko frontend par play karna.
    st.audio(to_wav_bytes(audio["bytes"]), format="audio/wav")

    # AI ko audio send karne ke liye button.
    if st.button("Send to AI Agent"):

        # Audio ko file format mein prepare karna.
        files = {
            "audio": (
                "recording.webm",
                audio["bytes"],
                "audio/webm"
            )
        }

        # AI processing ke time loading message show karna.
        with st.spinner("AI is processing your voice..."):

            # Recorded audio FastAPI backend ko send karna.
            response = requests.post(
                f"{API_URL}/api/voice",
                files=files,
                timeout=180
            )

        # Check karna ki API request successful hai ya nahi.
        if response.ok:

            # Backend se JSON response lena.
            result = response.json()

            # User ki converted speech show karna.
            st.write("**You said:**", result["user_text"])

            # AI ka generated text response show karna.
            st.write("**AI Response:**", result["reply"])

            # Backend se generated audio download karna.
            audio_response = requests.get(
                f"{API_URL}/api/voice/audio",
                timeout=30
            )

            # AI generated voice play karna.
            if audio_response.ok and audio_response.content:
                st.audio(
                    to_wav_bytes(audio_response.content),
                    format="audio/wav"
                )
            else:
                st.error("AI audio could not be loaded or was empty.")

        else:
            # API error show karna.
            st.error(response.text)
