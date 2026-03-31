import os
import dotenv
import streamlit as st
from openai import OpenAI

dotenv.load_dotenv()

try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TEMPLATE_FORMATS = {
    "SOAP": """\
Output format (SOAP Note):
Patient: [auto-fill from input]
Doctor: [auto-fill from input]
Date: [auto-fill from input]
Subjective (S) — Chief Complaint & HPI:
Objective (O) — Vitals, Exam findings, Labs:
Assessment (A) — Diagnosis / Differential:
Plan (P) — Medications, referrals, follow-up:""",

    "DAP": """\
Output format (DAP Note):
Patient: [auto-fill from input]
Doctor: [auto-fill from input]
Date: [auto-fill from input]
Data — Subjective and objective observations:
Assessment — Clinical interpretation and diagnosis:
Plan — Treatment, medications, follow-up actions:""",

    "Psychiatry": """\
Output format (Psychiatry Note):
Patient: [auto-fill from input]
Doctor: [auto-fill from input]
Date: [auto-fill from input]
Chief Complaint:
History of Present Illness:
Mental Status Exam (appearance, mood, affect, thought process, cognition, insight):
Risk Assessment (suicidality, homicidality, self-harm):
DSM-5 Diagnosis:
Treatment Plan (medication, therapy, safety plan, follow-up):""",

    "Pediatrics": """\
Output format (Pediatrics Note):
Patient: [auto-fill from input]
Doctor: [auto-fill from input]
Date: [auto-fill from input]
Chief Complaint:
HPI (include developmental history if relevant):
Growth & Development Milestones:
Immunization Status:
Physical Exam findings:
Assessment & Diagnosis:
Plan (medications with weight-based dosing, parent education, follow-up):""",
}


def get_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)