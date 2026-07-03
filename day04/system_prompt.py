from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

question = "What is the internet?"

personas = {
    "One sentence only": "Answer every question in exactly one sentence.",
    "Explain to a 7-year-old": "You explain everything as if talking to a 7-year-old child.",
    "Senior engineer": "You are a senior software engineer. Be technical and precise.",
}

for label, instruction in personas.items():
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"system",
                "content": instruction
            },
            {
                "role":"user",
                "content":question
            }
        ]
    )

    print(f"--- {label} ---")
    print(response.choices[0].message.content.strip())
    print()