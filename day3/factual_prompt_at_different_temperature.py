from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = "What is the capital of Australia?"

for temperature in [0.1, 1.4]:

    print(f"\n{'='*50}")
    print(f"Temperature: {temperature}")
    print(f"{'='*50}")

    for run in range(1,6):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature
        )

        print(
            f"Run {run+1}: "
            f"{response.choices[0].message.content.strip()}"
        )




'''
#gemini code

import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt = "What is the capital of Australia?"

for temperature in [0.1,1.4]:
    print(f"\n {'='*50}")
    print(f"Temperature: {temperature}")
    print(f"{'='*50}")
    
    for run in range(2):
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        )
        response = model.generate_content(prompt)
        print(f"Run {run}: {response.text.strip()}")

'''