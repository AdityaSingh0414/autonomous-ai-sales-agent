import streamlit as st
import requests

st.title("📊 Sales Analytics Dashboard")

try:
    response = requests.get(
        "http://127.0.0.1:8000/api/analytics",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Leads", data["total_leads"])
    col2.metric("Hot Leads", data["hot_leads"])
    col3.metric("Appointments", data["total_appointments"])

except requests.exceptions.RequestException:
    st.error("Unable to connect to backend.")