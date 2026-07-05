import os
import re
import json
import time
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

def evaluate_single(item, judge_model):
    user_prompt = f"""Question: {item['question']}
Expected answer: {item['expected']}
Actual answer: {item['actual']}
Context used (retrieved chunks):
{item.get('context', '')}

Score the actual answer on correctness and faithfulness."""

    while True:
        try:
            response = judge_model.generate_content(user_prompt)
            evaluation = json.loads(response.text.strip())
            return evaluation
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "ResourceExhausted" in error_str or "quota" in error_str.lower():
                retry_sec = 60.0
                match = re.search(r"Please retry in ([\d\.]+)s", error_str)
                if match:
                    retry_sec = float(match.group(1)) + 1.0
                else:
                    match2 = re.search(r"seconds:\s*(\d+)", error_str)
                    if match2:
                        retry_sec = float(match2.group(1)) + 1.0
                print(f"\n[Judge: Quota exceeded. Sleeping for {retry_sec:.1f}s before retrying...]")
                time.sleep(retry_sec)
            else:
                print(f"\n[Judge Error: {e}. Retrying in 5 seconds...]")
                time.sleep(5)

def main():
    if not os.path.exists("eval_results.json"):
        print("Error: eval_results.json not found.")
        return
        
    with open("eval_results.json", "r", encoding="utf-8") as f:
        eval_results = json.load(f)

    # Load existing scores if they exist, for resuming capability
    existing_scores = {}
    if os.path.exists("eval_scores.json"):
        try:
            with open("eval_scores.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if "correctness_score" in item:
                        existing_scores[item["question"]] = item
        except Exception as e:
            print(f"Warning: Could not parse existing eval_scores.json: {e}")

    # Setup Judge Model
    judge_model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=JUDGE_SYSTEM_PROMPT,
        generation_config={"response_mime_type": "application/json"}
    )

    print(f"Starting evaluation of {len(eval_results)} results...")
    scores = []
    
    for i, item in enumerate(eval_results, 1):
        question = item["question"]
        expected = item["expected"]
        actual = item["actual"]
        
        # Resume check
        if question in existing_scores:
            print(f"Q{i}: ✓ skipped (already scored) | {question}")
            scores.append(existing_scores[question])
            continue

        print(f"Evaluating Q{i}... ", end="", flush=True)
        eval_res = evaluate_single(item, judge_model)
        time.sleep(13)  # Standard sleep between evaluations
        print("✓ evaluated")

        scores.append({
            "question": question,
            "expected": expected,
            "actual": actual,
            "context": item.get("context", ""),
            "correctness_score": eval_res.get("correctness_score", 1),
            "correctness_reason": eval_res.get("correctness_reason", ""),
            "faithfulness_score": eval_res.get("faithfulness_score", 1),
            "faithfulness_reason": eval_res.get("faithfulness_reason", "")
        })

    # Save scores
    with open("eval_scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

    # Print summary
    print("\nEval complete. Results:")
    total_correctness = 0
    total_faithfulness = 0
    
    for i, item in enumerate(scores, 1):
        corr = item["correctness_score"]
        faith = item["faithfulness_score"]
        total_correctness += corr
        total_faithfulness += faith
        print(f"Q{i}: Correctness {corr}/5 | Faithfulness {faith}/5 | {item['question']}")

    avg_corr = total_correctness / len(scores)
    avg_faith = total_faithfulness / len(scores)
    
    print(f"Average correctness: {avg_corr:.1f} / 5.0")
    print(f"Average faithfulness: {avg_faith:.1f} / 5.0")

if __name__ == "__main__":
    main()