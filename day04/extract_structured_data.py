import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

records = [
    "Ahmed, 28, works as a backend developer in Lahore. Email: ahmed@dev.pk",
    "Sara is a UX designer based in Karachi, she's 31. Contact her at sara@ux.io",
    "Bilal (bilal@ml.com) is 25, studying machine learning in Islamabad",
]

for record in records:

    prompt = (
        "Extract the name, age, city, role and email from this text. "
        "Return JSON with keys: name, age, city, role, email. \n \n"
        f"{record}"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = [
            {
                "role":"system",
                "content": (
                    "You are a data extraction tool. "
                    "Always return valid JSON only. "
                    "No markdown. No explanations."
                )
            },
            {
                "role":"user",
                "content": prompt
            }
            
        ],
        temperature = 0
    )

    try:
        data = json.loads(
            response.choices[0].message.content
        )

        print(data)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for: {record}")

        print(response.choices[0].message.content)
    print()
