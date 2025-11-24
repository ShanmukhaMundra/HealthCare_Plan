import streamlit as st
from openai import OpenAI
from audiorecorder import audiorecorder
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import datetime
import os
import dotenv
dotenv.load_dotenv()


st.set_page_config(page_title="AI Medical Scribe", page_icon="🩺", layout="centered")
st.title("🩺 AI Medical Scribe - Speech to Text + Clinical Note Generator")

st.subheader("👩‍⚕️ Clinician & Patient Information")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("No OpenAI API key found.")
    st.warning("Make sure to set your OpenAI API key in the .env project file.")
    st.stop()


try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    st.success(" Everything looks good! You're ready to dive in.")
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    doctor_name = st.text_input("Doctor Name", value=" ")
    specialty = st.text_input("Specialty", value=" ")
with col2:
    patient_name = st.text_input("Patient Name", value=" ")
    patient_age = st.text_input("Patient Age / Gender", value=" ")

visit_date = st.date_input("Date of Visit", value=datetime.date.today())


st.session_state["doctor_name"] = doctor_name
st.session_state["specialty"] = specialty
st.session_state["patient_name"] = patient_name
st.session_state["patient_age"] = patient_age
st.session_state["visit_date"] = str(visit_date)

st.write("Record or Upload a doctor–patient conversation to generate a transcript and a structured clinical note.")


st.subheader("🎙️ Need to record audio? Click the button below.")
audio_data = audiorecorder("Start recording", "Stop Recording...")

if len(audio_data) > 0:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        audio_data.export(tmpfile.name, format="wav")
        temp_path = tmpfile.name

    st.audio(temp_path, format="audio/wav")

    if st.button("Transcribe Recording", key="record_button"):
        with st.spinner("Transcribing your recording..."):
            try:
                with open(temp_path, "rb") as f:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f
                    )

                text_output = transcript.text
                st.session_state["transcript"] = text_output
                st.success("Transcribed successfully!")
                st.text_area("Transcript", text_output, height=250)

            except Exception as e:
                st.error(f"Transcription failed: {e}")

audio_file = st.file_uploader("Upload Audio Below", type=["mp3", "wav", "m4a", "webm", "ogg", "flac"])

if audio_file:
    st.audio(audio_file, format="audio/mp3")

    if st.button("Transcribe", key="transcribe_button"):
        with st.spinner("Transcribing... please wait ⏳"):
            try:
                temp_path = f"temp_{audio_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(audio_file.read())

                with open(temp_path, "rb") as f:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f
                    )

                text_output = transcript.text
                st.session_state["transcript"] = text_output
                st.success("✅ Transcription complete!")
                st.text_area("Transcript", text_output, height=250)
                os.remove(temp_path)

            except Exception as e:
                st.error(f"Transcription failed: {e}")

if "transcript" in st.session_state:
    if st.button("Generate Clinical Note", key="note_button"):
        with st.spinner("Analyzing transcript to generate note 🧠..."):
            try:
                prompt = f"""
                You are a clinical documentation assistant.
                Use the provided patient and doctor information to produce a structured SOAP note
                from the conversation transcript below.

                Doctor: {st.session_state['doctor_name']}
                Specialty: {st.session_state['specialty']}
                Patient: {st.session_state['patient_name']}
                Age/Gender: {st.session_state['patient_age']}
                Date: {st.session_state['visit_date']}

                Transcript:
                {st.session_state['transcript']}

                Output format:
                Patient: [auto-fill from input]
                Doctor: [auto-fill from input]
                Date: [auto-fill from input]
                CC:
                HPI:
                Assessment:
                Plan:
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                note = response.choices[0].message.content
                st.session_state["note"] = note

                st.success("Clinical note generated successfully!")
                st.text_area("Structured Clinical Note", note, height=350)

            except Exception as e:
                st.error(f"Error generating clinical note: {e}")

if "note" in st.session_state:
    if st.button("📄 Download Clinical Note as PDF", key="pdf_button"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                c = canvas.Canvas(tmpfile.name, pagesize=letter)
                width, height = letter

                c.setFont('Helvetica-Bold', 12)
                c.drawString(72, height - 100,f"Doctor: {st.session_state['doctor_name']} ({st.session_state['specialty']})")
                c.drawString(72, height - 130,f"Patient: {st.session_state['patient_name']} | Age/Gender: {st.session_state['patient_age']}")
                c.drawString(72, height - 150, f"Date: {st.session_state['visit_date']}")

                c.setFont("Helvetica", 11)
                text = st.session_state["note"]
                y = height - 100
                for line in text.split("\n"):
                    if y < 72:
                        c.showPage()
                        c.setFont("Aptos", 12)
                        c.drawString(
                            72, height - 72, "AI Medical Scribe - Clinical Note"
                        )
                        y = height - 72
                    c.drawString(72, y, line)
                    y -= 15

                c.save()

                with open(tmpfile.name, "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    b64 = base64.b64encode(pdf_data).decode("utf-8")

                href = f'<a href="data:application/pdf;base64,{b64}" download="Clinical-Note.pdf">📥 need a copy..click here</a>'
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error creating PDF: {e}")