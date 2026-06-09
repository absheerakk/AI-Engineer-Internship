import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

history = []

turns = [
    "My favourite programming language is Python.",
    "I am learning AI engineering.",
    "What is my favourite programming language?",
    "What am I currently learning?",
]

for user_message in turns:

    history.append(
        {
        "role":"user",
        "content":user_message
        }
    )

    response= client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"system",
                "content":"You are a helpful assisant wth a good memory."
            },
            *history
        ]
    )

    reply = response.choices[0].message.content.strip()

    history.append(
        {
            "role":"assistant",
            "content": reply #important
        }
    )

    print(f"User:{user_message}")
    print(f"Model: {reply}")
    print()