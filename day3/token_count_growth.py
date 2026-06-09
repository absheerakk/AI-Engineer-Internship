import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

TOKEN_LIMIT = 300
message = "The customer asked about the refund policy and we explained it takes 5 to 7 business days."

messages = []
for turn in range(1,20):
    messages.append(message)
    combined ="".join(messages)
    total = model.count_tokens(combined).total_tokens
    print(f"Turn {turn:>2} | Tokens so far: {total}")

    if total >= TOKEN_LIMIT:
        print(f"\n Hit the limit at turn {turn}. Older messages would start falling off here.")
        break