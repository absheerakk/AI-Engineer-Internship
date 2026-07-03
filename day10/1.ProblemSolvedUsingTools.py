import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

questions = [ "What is 17 multiplied by 38, then divided by 4? Show your working.",
        "What is the square root of 1764?",
        "What day of the week is 15 August 2047?"
]

for q in questions:
    response = model.generate_content(q)

    print(f"Q: {q}")
    print(f"A: {response.text.strip()}")
    print("-" * 50)