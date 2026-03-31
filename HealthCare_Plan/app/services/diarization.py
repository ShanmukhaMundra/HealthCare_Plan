from openai import OpenAI


def diarize(client: OpenAI, raw_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                "You are a medical transcription specialist.\n"
                "Re-format the transcript below by labeling each speaker turn as either "
                "'Doctor:' or 'Patient:' based on context clues (questions, clinical language, "
                "symptom descriptions, etc.). Preserve the exact words spoken — do not "
                "summarize or paraphrase. Output only the labeled transcript, one turn per line.\n\n"
                f"Transcript:\n{raw_text}"
            )
        }]
    )
    return response.choices[0].message.content