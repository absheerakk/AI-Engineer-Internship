import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    generation_config=genai.types.GenerationConfig(temperature=0.3)
)

def summarise_prompt(text, max_Sentences=3, audience="general"):
    return(
        f"summarise the following text in{max_Sentences} sentences or fewer."
        f"write for a {audience} audience. Be clear and direct. \n\n {text}"
    )

texts = [
    (
        "Machine learning is a subset of artificial intelligence that gives systems "
        "the ability to learn from data without being explicitly programmed. "
        "It focuses on building programs that improve automatically through experience. "
        "Applications include image recognition, language translation, and recommendation systems.",
        2,
        "non-technical",
    ),
    (
        "Gradient descent is an optimisation algorithm used to minimise a function by "
        "iteratively moving in the direction of steepest descent as defined by the "
        "negative of the gradient. It is widely used in training neural networks.",
        2,
        "technical",
    ),
]

for text, sentences, audience in texts:
    prompt = summarise_prompt(text, max_Sentences=sentences, audience=audience)
    response = model.generate_content(prompt)
    print(f"Audience: {audience}")
    print(response.text.strip())
    time.sleep(45)
    print()