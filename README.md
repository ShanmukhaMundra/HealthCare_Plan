# AI Medical Scribe

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://healthcareplan-b4ggvtycf2wxqx3jv9rxa2.streamlit.app/)

A Streamlit web app that converts doctor-patient conversations into structured clinical notes using OpenAI Whisper for transcription and GPT-4o-mini for note generation.

**[Try the live app →](https://healthcareplan-b4ggvtycf2wxqx3jv9rxa2.streamlit.app/)**

## Features

- **Audio transcription** — record live audio or upload a file; transcribed via OpenAI Whisper
- **Speaker diarization** — GPT-4o-mini labels each turn as `Doctor:` or `Patient:`
- **Clinical note generation** — produces structured notes in four formats:
  - SOAP (Subjective, Objective, Assessment, Plan)
  - DAP (Data, Assessment, Plan)
  - Psychiatry
  - Pediatrics
- **PDF export** — download the generated note as a formatted PDF

## Project Structure

```
HealthCare_Plan/
├── main_app.py           
├── requirements.txt
├── app/
│   ├── config.py            
│   ├── services/
│   │   ├── transcription.py 
│   │   ├── diarization.py   
│   │   └── note_generator.py
│   └── ui/
│       ├── patient_info.py  
│       ├── audio.py        
│       ├── clinical_note.py 
│       └── pdf_export.py    
└── tests/
    └── test_prompt.py
```

## Setup

**1. Clone the repo and install dependencies**

```bash
pip install -r requirements.txt
```

**2. Set your OpenAI API key**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
```

**3. Run the app**

```bash
streamlit run main_app.py
```

## Usage

1. Fill in the patient and doctor details in the sidebar form.
2. Record audio or upload an audio file of the conversation.
3. Transcribe the audio — the app will also label Doctor/Patient turns.
4. Select a note template and generate the clinical note.
5. Download the note as a PDF.

## Screenshots

**Audio upload with speaker diarization option**

<img width="1440" height="900" alt="Screenshot 2026-03-30 at 8 04 15 PM" src="https://github.com/user-attachments/assets/a8bc3d38-c987-4c6c-99c6-c2b9ff61e96f" />


**Audio uploaded and ready to transcribe**

<img width="1440" height="900" alt="Screenshot 2026-03-30 at 8 04 30 PM" src="https://github.com/user-attachments/assets/af83c3a2-39a5-46a2-b4b9-5ff8f3579468" />


**SOAP note generated from transcript**

<img width="1440" height="900" alt="Screenshot 2026-03-30 at 8 04 41 PM" src="https://github.com/user-attachments/assets/93990b7c-d9ba-4b3d-9e65-824f3d6fee9b" />


**Full note with Assessment & Plan + PDF download**

<img width="1440" height="900" alt="Screenshot 2026-03-30 at 8 04 49 PM" src="https://github.com/user-attachments/assets/bc92cb31-16f9-4a6a-a066-c404cd9853fe" />


## Requirements

- Python 3.9+
- OpenAI API key with access to `whisper-1` and `gpt-4o-mini`
