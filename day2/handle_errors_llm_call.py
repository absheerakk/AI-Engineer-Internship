'''
Exercise 05 — Handle Errors Gracefully
Improve your script from Exercise 4 so it never crashes with an ugly traceback. Check for a missing key
before making the call, and wrap the API call in a try/except block.
• Check if the key exists right after loading it. If not, print a clear message and exit.
• Wrap your generate_content call in a try block.
• In the except block, print the error message in a readable format.
• Test it by temporarily using a wrong API key.
Note: Good error handling is what separates a script from a real tool.
Bonus: Look up the specific exception that Google's library raises when a quota is exceeded. Add a
separate except block just for that case.

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

try:
    response = model.generate_content("Why is giraffe's neck so long?")
    print("why giraffe's neck is so long?: \n", response.text)

except ResourceExhausted:
    print("Quota Exceeded.")

except Exception as e:
    print(f"Gemini API Error: {e}")