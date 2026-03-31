import datetime
import streamlit as st


def render():
    st.divider()
    st.subheader("👩‍⚕️ Clinician & Patient Information")

    col1, col2 = st.columns(2)
    with col1:
        doctor_name = st.text_input("Doctor Name", value=" ")
        specialty = st.text_input("Specialty", value=" ")
    with col2:
        patient_name = st.text_input("Patient Name", value=" ")
        patient_age = st.text_input("Patient Age / Gender", value=" ")

    visit_date = st.date_input("Date of Visit", value=datetime.date.today())

    st.markdown("**Prior Medical History (optional)**")
    patient_history = st.text_area(
        "Prior conditions, current medications, known allergies",
        height=100,
        placeholder="e.g. Type 2 diabetes, hypertension / Metformin 500mg, Lisinopril 10mg / Penicillin allergy",
        key="patient_history_input"
    )

    st.session_state["doctor_name"] = doctor_name
    st.session_state["specialty"] = specialty
    st.session_state["patient_name"] = patient_name
    st.session_state["patient_age"] = patient_age
    st.session_state["visit_date"] = str(visit_date)
    st.session_state["patient_history"] = patient_history