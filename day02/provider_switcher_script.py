'''
Exercise 10 — Build a Provider-Switcher Script
Combine your Gemini and Ollama scripts into one. Ask the user to choose a provider at the start, then
route their question to the right model. This is your Day 2 mini-capstone.
• Print a menu asking the user to choose between Gemini (cloud) and Ollama (local).
• Read their choice with input().
• Ask for a question, then call either your Gemini function or your Ollama function depending on the
choice.
• Print the answer with a label showing which provider responded.
Note: This pattern — swapping providers behind a common interface — is how real AI apps are built to be
model-agnostic.
Bonus: Add a third option that sends the same question to both providers and prints both answers side by
side for comparison.

'''

import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests


#gemini
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: Gemini API Key not found.")
    exit()
    
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

#functiion - gemini
def ask_gemini(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"
    
#function - ollama

def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
          "model":"gemma3:1b",
          "prompt":prompt,
          "stream": False
    }
    response = requests.post(url,json=payload)
    data = response.json()

    return data["response"]

print("----------Provider-switcher----------")
print("1. Gemini")
print("2. Ollama")
print("3. Compare Both")

choice = input("\nChoose a provider: ")

question = input("\n Ask the question: ")

if choice=="1":

    answer = ask_gemini(question)

    print("\n You chose GEMINI.")
    print("------------------")
    print(answer)

elif choice=="2":

    answer = ask_ollama(question)

    print("\n You chose OLLAMA.")
    print("------------------")
    print(answer)

elif choice=="3":
    gemini_answer = ask_gemini(question)
    ollama_answer = ask_ollama(question)

    print("\n ==========GEMINI==========")
    print(gemini_answer)

    print("\n ==========OLLANA==========")
    print(ollama_answer)

else:
    print("Invalid choice")
