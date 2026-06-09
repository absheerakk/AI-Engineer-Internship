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
        "You are a helpful assistant. Answer questions using only the context provided. "
        "If the answer is not in the context, say 'I don't have that information.'"
    ),
)

# ── Ingestion ────────────────────────────────────────────────────

def load_and_chunk(filepath, chunk_size=3):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = ". " .join(sentences[i:i + chunk_size]) + "."
        chunks.append(chunk)
    return chunks

def build_collection(chunks, embed_model):
    client = chromadb.Client()
    collection = client.create_collection("knowledge_base")
    embeddings = embed_model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    return collection

# ── Retrieval ────────────────────────────────────────────────────
def retrieve(question, collection, embed_model, top_k=3):
    query_embedding = embed_model.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0]

# ── Generation ───────────────────────────────────────────────────
def build_prompt(question, chunks):
    context = "\n\n".join(f"- {chunk}" for chunk in chunks)
    return f"Context:\n{context}\n\nQuestion: {question}"

def rag(question, collection, embed_model, llm):
    chunks = retrieve(question, collection, embed_model)
    prompt = build_prompt(question, chunks)
    response = llm.generate_content(prompt)
    return response.text.strip(), chunks

# ── Main ─────────────────────────────────────────────────────────
chunks = load_and_chunk("knowledge.txt")
collection = build_collection(chunks, embed_model)
print(f"Loaded {len(chunks)} chunks from knowledge.txt\n")

print("Ask questions about your document. Type 'quit' to exit.\n")

while True:
    question = input("Q: ").strip()
    if not question:
        continue
    if question.lower() == "quit":
        break

    answer, used_chunks = rag(question, collection, embed_model, llm)
    print(f"\nA: {answer}\n")
    print("Sources used:")
    for chunk in used_chunks:
        print(f"  - {chunk[:100]}...")
    print()
