import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

problem = (
    "A shop sells apples for Rs 40 each and oranges for Rs 25 each. "
    "Ali buys 3 apples and 5 oranges. He pays with a Rs 500 note. "
    "How much change does he get?"
)

direct = f"{problem}\n\nWhat is the answer?"
cot    = f"{problem}\n\nThink through this step by step, then give the final answer."

print("--- Direct answer ---")
print(model.generate_content(direct).text.strip())

print("\n--- Chain-of-thought ---")
print(model.generate_content(cot).text.strip())
