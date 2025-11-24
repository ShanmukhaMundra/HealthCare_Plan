from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
prompt = f'''You are a responsible AI. what happens when a patient gets high BP. give answer in a shorter description'''

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

note = response.choices[0].message.content
print(note)