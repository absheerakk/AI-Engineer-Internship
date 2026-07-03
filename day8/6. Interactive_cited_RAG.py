import os
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
llm = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
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
    collection = client.create_collection("interactive_rag")
    collection.add(
        documents=chunks,
        embeddings=embed_model.encode(chunks).tolist(),
        ids=[f"c_{i}" for i in range(len(chunks))],
    )
    return collection, len(chunks)

def ask(question, collection):
    results = collection.query(
        query_embeddings=embed_model.encode([question]).tolist(),
        n_results=3,
    )
    used_chunks = results["documents"][0]
    context = "\n\n".join(f"- {c}" for c in used_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    answer = llm.generate_content(prompt).text.strip()
    return answer, used_chunks

collection, total_chunks = load_and_index("day8/knowledge.txt")
print(f"Loaded knowledge.txt — {total_chunks} chunks indexed.\n")
print("Ask questions. Type 'quit' to exit.\n")

while True:
    question = input("Q: ").strip()
    if not question:
        continue
    if question.lower() == "quit":
        break

    answer, sources = ask(question, collection)
    print(f"\nA: {answer}\n")
    print("Sources:")
    for i, source in enumerate(sources, 1):
        print(f"  [{i}] {source[:120]}...")
    print()
