import os
import json
import time
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize models
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
llm = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction=(
        "Answer using only the context provided. "
        "If the answer is not in the context, say 'I don't have that information.'"
    ),
)

def overlapping_chunks(text, n=3, overlap=1):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    step = n - overlap
    chunks = []
    for i in range(0, len(sentences), step):
        group = sentences[i:i + n]
        if group:
            chunks.append(". ".join(group) + ".")
    return chunks

def load_and_index(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = overlapping_chunks(text, n=3, overlap=1)
    client = chromadb.Client()
    collection = client.create_collection("eval_rag")
    collection.add(
        documents=chunks,
        embeddings=embed_model.encode(chunks).tolist(),
        ids=[f"c_{i}" for i in range(len(chunks))],
    )
    return collection

def ask(question, collection):
    results = collection.query(
        query_embeddings=embed_model.encode([question]).tolist(),
        n_results=3,
    )
    used_chunks = results["documents"][0]
    context = "\n\n".join(f"- {c}" for c in used_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    
    # Retry logic for robustness
    for _ in range(3):
        try:
            response = llm.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error during API call: {e}. Retrying in 2 seconds...")
            time.sleep(2)
    return "Error generating response."

def main():
    # 1. Load eval set
    if not os.path.exists("eval_set.json"):
        print("Error: eval_set.json not found.")
        return
        
    with open("eval_set.json", "r", encoding="utf-8") as f:
        eval_set = json.load(f)
        
    # 2. Load and index document
    print("Loading knowledge.txt and building index...")
    collection = load_and_index("python.txt")
    
    # 3. Run eval set
    print(f"Running eval set ({len(eval_set)} questions)...")
    results = []
    
    for i, item in enumerate(eval_set, 1):
        question = item["question"]
        expected = item["expected"]
        context = item.get("context", "")
        
        print(f"[{i}/{len(eval_set)}] {question} ", end="", flush=True)
        
        actual = ask(question, collection)
        time.sleep(13)  # Rate limit sleep
        
        print("✓ answered")
        
        results.append({
            "question": question,
            "expected": expected,
            "actual": actual,
            "context": context,
            "in_document": expected.lower() != "i don't have that information."
        })
        
    # 4. Save results
    with open("eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print("Done. Results saved to eval_results.json")

if __name__ == "__main__":
    main()