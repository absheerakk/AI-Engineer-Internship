'''
Exercise 06 — Build an Interactive Question Script
Extend your script to take a question from the user at runtime using input(), then send it to Gemini and
print the answer.
• Use input() to prompt the user for a question.
• Strip whitespace from the input.
• If the input is empty, print a message and exit cleanly.
• Otherwise, send it to the API and print the result.
Note: Run it and ask at least 3 different questions.
Bonus: Run the same question three times in a row and notice the answer changes slightly each time.
This is the model's randomness, called temperature, in action.

'''


import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    exit()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = input("Enter the prompt: ").strip()

if len(prompt)==0:
    print("ERROR: Empty prompt.")
    exit()
else:
    response = model.generate_content(prompt)
    print(response.text)
