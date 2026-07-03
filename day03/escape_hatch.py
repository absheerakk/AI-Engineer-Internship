from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

prompt_a = "What was the exact population of Lahore in 1923?"

prompt_b = (
    "What was the exact population of Lahore in 1923? "
    "If you are not certain, say so and explain what you do know."
)

print("--- No escape hatch ---")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt_a}
    ],
    temperature=0.7
)

print(response.choices[0].message.content.strip())

print("\n--- With escape hatch ---")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt_b}
    ],
    temperature=0.7
)

print(response.choices[0].message.content.strip())