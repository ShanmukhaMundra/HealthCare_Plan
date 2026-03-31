from openai import OpenAI
from app.config import TEMPLATE_FORMATS


def generate_note(client: OpenAI, context: dict, transcript: str, template: str) -> str:
    history_raw = context.get("patient_history", "").strip()
    history_section = f"Patient History:\n{history_raw}\n" if history_raw else ""
    output_format = TEMPLATE_FORMATS.get(template, TEMPLATE_FORMATS["SOAP"])

    prompt = f"""You are a clinical documentation assistant.
Use the provided patient and doctor information to produce a structured clinical note
from the conversation transcript below.

Doctor: {context['doctor_name']}
Specialty: {context['specialty']}
Patient: {context['patient_name']}
Age/Gender: {context['patient_age']}
Date: {context['visit_date']}
{history_section}
Transcript:
{transcript}

{output_format}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content