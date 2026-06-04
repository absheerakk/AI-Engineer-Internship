'''
Exercise 07 — Ask Multiple Questions in a Loop
Modify your script to keep asking for questions in a loop until the user decides to quit, instead of exiting
after a single answer.
• Wrap your input and API call inside a while True loop.
• If the user types quit or exit, break out of the loop with a goodbye message.
• If the input is empty, skip the API call and prompt again.
• Otherwise, send the question and print the answer, then loop back.
Note: Notice that the model does not remember your earlier questions — each call is independent. Day 6
covers how to fix this with conversation history.
Bonus: Count how many questions the user has asked and print the total when they exit.

'''

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    exit()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")
count = 0

while True:
    prompt = input("Enter a question: ").strip()

    if prompt.lower() in ["quit", "exit"]:
        print(f"\n You asked {count} questions.")
        break
    if not prompt.strip():
        print("Please enter a question.")
        continue
    else:
        try:
            response = model.generate_content(prompt)
            print(response.text)
            count +=1
            
        except ResourceExhausted:
            print("Quota Exceeded.")

        except Exception as e:
            print(f"Gemini API Error: {e}")
            
