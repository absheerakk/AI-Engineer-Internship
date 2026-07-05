import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Hardcoded Judge System Prompt
JUDGE_SYSTEM_PROMPT = """You are an expert AI evaluator playing the role of a judge model. Your task is to evaluate a question-answering system's actual answer against an expected answer (ground truth) and the provided context.

You must evaluate the actual answer on two dimensions: Correctness and Faithfulness.

---
DIMENSION 1: Correctness
Compare the actual answer to the expected answer. Does the actual answer convey the same factual information as the expected answer?

Scoring Rubric:
- 5: Completely correct. All key facts, numbers, and relationships match. Minor grammatical differences are allowed.
- 4: Mostly correct. Minor details may be omitted, but the main factual answer is correct and no incorrect facts are added.
- 3: Partially correct. Some key facts are right, but important facts are missing or some details are incorrect.
- 2: Mostly incorrect. The actual answer misses the majority of key facts but has a minor piece of truth.
- 1: Incorrect or completely missing the point. The answer is completely wrong, irrelevant, or says "I don't have that information" when the document actually had the answer.

---
DIMENSION 2: Faithfulness
Compare the actual answer to the provided context. Is the actual answer grounded strictly in the context, or does it add outside information or hallucinate facts?

Scoring Rubric:
- 5: Fully faithful. Everything in the actual answer comes directly and strictly from the provided context. No outside knowledge or ungrounded assumptions are added.
- 4: Mostly faithful. The answer is grounded, but uses slight rephrasing or minor logical connections that are highly plausible based on the context but not explicitly stated.
- 3: Partially faithful. The answer is mostly grounded, but adds one or two minor details from outside knowledge that were not in the provided context.
- 2: Mostly unfaithful. The answer adds major outside details, makes large ungrounded assumptions, or contradicts minor details of the context.
- 1: Unfaithful. The answer directly contradicts the provided context, invents facts, or is completely based on outside knowledge.

---
JSON OUTPUT FORMAT:
You must output ONLY a valid JSON object in the following format. Do not add any markdown formatting, explanation, or extra characters outside of this JSON block:

{
  "correctness_score": <int: 1-5>,
  "correctness_reason": "<string: detailed explanation of correctness scoring>",
  "faithfulness_score": <int: 1-5>,
  "faithfulness_reason": "<string: detailed explanation of faithfulness scoring>"
}
"""

def main():
    # Load first item from eval_results.json
    if not os.path.exists("eval_results.json"):
        print("Error: eval_results.json not found. Run evaluation first.")
        return
        
    with open("eval_results.json", "r", encoding="utf-8") as f:
        eval_results = json.load(f)
        first_item = eval_results[0]

    # Setup Judge Model (forcing JSON mime type)
    judge_model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=JUDGE_SYSTEM_PROMPT,
        generation_config={"response_mime_type": "application/json"}
    )

    user_prompt = f"""Question: {first_item['question']}
Expected answer: {first_item['expected']}
Actual answer: {first_item['actual']}
Context used (retrieved chunks):
{first_item.get('context', '')}

Score the actual answer on correctness and faithfulness."""

    try:
        response = judge_model.generate_content(user_prompt)
        evaluation = json.loads(response.text.strip())
        
        print(f"Question: {first_item['question']}")
        print(f"Expected: {first_item['expected']}")
        print(f"Actual: {first_item['actual']}")
        print(f"Correctness: {evaluation.get('correctness_score')}/5")
        print(f"Reason: {evaluation.get('correctness_reason')}")
        print(f"Faithfulness: {evaluation.get('faithfulness_score')}/5")
        print(f"Reason: {evaluation.get('faithfulness_reason')}")

    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == "__main__":
    main()