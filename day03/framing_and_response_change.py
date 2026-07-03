import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

prompts = {
    "Clinical framing": "Patient presents with fever, cough, and fatigue.",
    "Casual framing": "I have a fever, cough, and fatigue. What should I do?",
}

for label,prompt in prompts.items():
    response = model.generate_content(prompt)
    print(f"------{label}------")
    print(response.text)
    print()
