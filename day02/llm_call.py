'''
Exercise 04 — Make Your First LLM Call
Write a script that sends one question to the Gemini API and prints the answer. This is your first real
interaction with a language model through your own code.
• Load your API key from .env.
• Configure the google.generativeai library with the key.
• Create a model object using gemini-1.5-flash.
• Send a simple question using generate_content and print the response text.
Note: You won't fully understand every line yet — that's fine. By Week 2 you will.
Bonus: After the call, print the usage metadata from the response. It shows the number of tokens used,
which is how the API measures cost and limits.

'''

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

#LOAD -> configre gemni -> create model -> send prompt -> recieve response
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    exit()

genai.configure(api_key=api_key) 

model = genai.GenerativeModel("gemini-2.5-flash") #(model generation)

response = model.generate_content("why giraffe's neck is so long?")

print("why giraffe's neck is so long?: \n", response.text)

print("\nUsage Metadata:")
print(response.usage_metadata)