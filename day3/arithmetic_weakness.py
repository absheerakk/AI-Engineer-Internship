from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

problems = [
    ("17 * 38", 17 * 38),
    ("127 + 486", 127 + 486),
    ("1024 / 16", 1024 / 16),
    ("333 * 27", 333 * 27),
    ("99999 + 1", 99999 + 1),
]

print(f"{'Problem':<20} {'Expected':>10} {'Model said':>15} {'OK?':>6}")
print("-" * 55)

for expression, expected in problems:

    prompt = (
        f"What is {expression}? "
        f"Reply with only the number, nothing else."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    model_answer = response.choices[0].message.content.strip()

    try:
        correct = abs(float(model_answer) - float(expected)) < 0.01
    except ValueError:
        correct = False

    print(
        f"{expression:<20} "
        f"{expected:>10} "
        f"{model_answer:>15} "
        f"{'✓' if correct else '✗':>6}"
    )