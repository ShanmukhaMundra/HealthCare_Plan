import os
import tempfile
import streamlit as st
from audiorecorder import audiorecorder
from openai import OpenAI
from app.services.transcription import transcribe
from app.services.diarization import diarize


def render(client: OpenAI):
    st.divider()
    st.subheader("🎙️ Record Audio")

    audio_data = audiorecorder("Start recording", "Stop Recording...")

    if len(audio_data) > 0:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            audio_data.export(tmpfile.name, format="wav")
            temp_path = tmpfile.name

        st.audio(temp_path, format="audio/wav")

        apply_diarization = st.checkbox(
            "Label speakers as Doctor / Patient", value=True, key="diarize_record"
        )

        if st.button("Transcribe Recording", key="record_button"):
            with st.spinner("Transcribing your recording..."):
                try:
                    text_output = transcribe(client, temp_path)

                    if apply_diarization:
                        with st.spinner("Identifying speakers..."):
                            text_output = diarize(client, text_output)

                    st.session_state["transcript"] = text_output
                    st.success("Transcribed successfully!")
                    st.text_area("Transcript", text_output, height=250)

                except Exception as e:
                    st.error(f"Transcription failed: {e}")

    # ── Upload ────────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📂 Upload Audio")

    audio_file = st.file_uploader("Upload Audio Below", type=["mp3", "wav", "m4a", "webm", "ogg", "flac"])

    if audio_file:
        st.audio(audio_file, format="audio/mp3")

        apply_diarization = st.checkbox(
            "Label speakers as Doctor / Patient", value=True, key="diarize_upload"
        )

        if st.button("Transcribe", key="transcribe_button"):
            with st.spinner("Transcribing... please wait ⏳"):
                try:
                    temp_path = f"temp_{audio_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(audio_file.read())

                    text_output = transcribe(client, temp_path)
                    os.remove(temp_path)

                    if apply_diarization:
                        with st.spinner("Identifying speakers..."):
                            text_output = diarize(client, text_output)

                    st.session_state["transcript"] = text_output
                    st.success("✅ Transcription complete!")
                    st.text_area("Transcript", text_output, height=250)

                except Exception as e:
                    st.error(f"Transcription failed: {e}")