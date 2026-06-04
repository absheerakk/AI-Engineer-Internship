'''
Exercise 03 — Load and Verify Your Key in Python
Write a script that loads your API key from the .env file using python-dotenv, then prints only the first 6
characters to confirm it loaded without exposing the full key.
• Import os and load_dotenv from the dotenv package.
• Call load_dotenv() then read the key with os.getenv.
• Print a message confirming the key loaded, showing only the first 6 characters.
• Add an else branch that prints a helpful error if the key is missing.
Note: Never print the full key — even in a terminal that others might see.
Bonus: Temporarily rename your .env file and run the script again. Observe the error message, then
rename it back.

'''

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print(f"API key loaded successfully: {api_key[:6]}******")
else:
    print("Error: GEMINI_API_KEY not found.")