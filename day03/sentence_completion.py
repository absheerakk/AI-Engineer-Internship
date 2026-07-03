import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

fragments = [
    "The mitochondria is the powerhouse of the",
    "To be, or not to be, that is the",
    "In Python, to open a file you use the",
    "The capital of Australia is",
]
for fragment in fragments:
    response = model.generate_content(fragment)
    print(f"PROMPT: {fragment}")
    print(f"COMPLETION: {response.text.strip()}")
    print()