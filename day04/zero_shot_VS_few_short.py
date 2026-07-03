from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

reviews = [
    "The battery lasts forever, really impressed.",
    "Stopped working after two weeks. Total waste.",
    "It is okay I guess, nothing special.",
    "Absolutely love it, using it every day!",
    "Not what I expected based on the description.",
]

zero_shot = """
classify this review as positive, negative, or neutral.
Reply with one word only.

Review: {review}
"""

few_shot = """
classify this review as positive, negative, or neutral.
Reply with one word only.

Examples:
Review: "Best purchase I have made this year." → positive
Review: "Completely fell apart after one use." → negative
Review: "Does the job, nothing more." → neutral

Review: {review}
"""

print(f"{'Review':<50} {'Zero-shot':>12} {'Few-shot':>12}")
print("-" * 76)

for review in reviews:
    r0 = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages= [
            {
                "role":"user",
                "content":zero_shot.format(review=review)
            }
        ],
        temperature=0
    )

    rf = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":few_shot.format(review=review)
            }
        ],
        temperature=0
    )

    zero_answer = r0.choices[0].message.content.strip()
    few_answer = rf.choices[0].message.content.strip()

    print(
        f"{review:<50}"
        f"{zero_answer:>12}"
        f"{few_answer:>12}"
    )
