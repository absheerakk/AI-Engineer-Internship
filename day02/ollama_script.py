'''
Exercise 09 — Call Ollama from Python
Write a Python script that sends a question to your local Ollama model using the requests library.
Compare the code structure with your Gemini script.
• Install the requests library if it is not already in your venv.
• Write a function that sends a POST request to the local Ollama API endpoint with the model name
and prompt.
• Parse the response JSON and return the answer text.
• Use input() to ask the user for a question, call your function, and print the answer.
Note: Make sure Ollama is running before executing this script. It starts automatically after install on most
systems.
Bonus: Ask Ollama the same question three times and see if the answers vary like Gemini's did.

'''


import requests

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

question = input("Enter a question to ask to ollama: ")

answer = ask_ollama(question)
print(answer)