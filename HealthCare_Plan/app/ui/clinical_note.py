import streamlit as st
from openai import OpenAI
from app.config import TEMPLATE_FORMATS
from app.services.note_generator import generate_note


def render(client: OpenAI):
    if "transcript" not in st.session_state:
        return

    st.divider()
    st.subheader("🧠 Clinical Note")

    st.selectbox(
        "Select Note Template",
        list(TEMPLATE_FORMATS.keys()),
        key="template"
    )

    if st.button("Generate Clinical Note", key="note_button"):
        with st.spinner("Analyzing transcript to generate note 🧠"):
            try:
                context = {
                    "doctor_name": st.session_state.get("doctor_name", ""),
                    "specialty": st.session_state.get("specialty", ""),
                    "patient_name": st.session_state.get("patient_name", ""),
                    "patient_age": st.session_state.get("patient_age", ""),
                    "visit_date": st.session_state.get("visit_date", ""),
                    "patient_history": st.session_state.get("patient_history", ""),
                }

                note = generate_note(
                    client=client,
                    context=context,
                    transcript=st.session_state["transcript"],
                    template=st.session_state.get("template", "SOAP"),
                )

                st.session_state["note"] = note
                st.success("Clinical note generated successfully!")
                st.text_area("Structured Clinical Note", note, height=350)

            except Exception as e:
                st.error(f"Error generating clinical note: {e}")