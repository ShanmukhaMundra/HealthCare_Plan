import streamlit as st
from app.config import OPENAI_API_KEY, get_client
from app.ui import patient_info, audio, clinical_note, pdf_export

st.set_page_config(page_title="AI Medical Scribe", page_icon="🩺", layout="centered")
st.title("🩺 AI Medical Scribe - Speech to Text + Clinical Note Generator")
st.write("Record or upload a doctor–patient conversation to generate a transcript and a structured clinical note.")

if not OPENAI_API_KEY:
    st.warning("Check OpenAI API key properly.")
    st.stop()

try:
    client = get_client()
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    st.stop()

patient_info.render()
audio.render(client)
clinical_note.render(client)
pdf_export.render()