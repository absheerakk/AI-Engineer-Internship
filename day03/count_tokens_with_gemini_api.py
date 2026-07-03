import os
import google.generativeai as genai 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

strings = [
    "Hello, world!",
    "The quick brown fox jumps over the lazy dog.",
    "Supercalifragilisticexpialidocious is a word from a 1964 film.",
    "x=1;y=2;z=x+y;print(z)",
    "Patient presents with a fever of 38.9 degrees, dry cough, and fatigue for 3 days."
]

for s in strings:
    result = model.count_tokens(s)
    print(f"{result.total_tokens:>4} tokens | {s}") #right aligned in a field with 4 spaces