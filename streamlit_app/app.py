
import streamlit as st
from utils.api_client import send_message


st.set_page_config(
    page_title="AI Sales Agent",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Autonomous AI Sales Agent")
st.caption("Your intelligent AI-powered sales assistant")
st.divider()


# Chat history initialize kar rahe hain.
if "messages" not in st.session_state:
    st.session_state.messages = []


# Previous messages display kar rahe hain.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User se message input le rahe hain.
user_input = st.chat_input(
    "Ask me about products, pricing or services..."
)


if user_input:

    # User ka message history mein save kar rahe hain.
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI ka response display kar rahe hain.
    with st.chat_message("assistant"):

        with st.spinner("Sales agent is thinking..."):

            # Previous conversation history copy kar rahe hain.
            # Current message already history mein add ho chuka hai,
            # isliye usko dobara add nahi karna hai.
            history = st.session_state.messages[:-1].copy()

            # User message aur previous history backend ko bhej rahe hain.
            reply = send_message(user_input, history)

            st.markdown(reply)

    # AI ka response chat history mein save kar rahe hain.
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
