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

document = """
Python was created by Guido van Rossum and first released in 1991.
It is an interpreted, high-level, general-purpose programming language.
Python's design philosophy emphasises code readability and simplicity.
It supports multiple programming paradigms including procedural, object-oriented, and functional programming.
Python has a large standard library and an active community.
It is widely used in web development, data science, machine learning, and automation.
The name Python comes from the BBC television show Monty Python's Flying Circus.
Python 2 reached end of life in 2020 and Python 3 is the current standard.
Popular Python frameworks include Django and Flask for web development.
NumPy, Pandas, and Scikit-learn are widely used for data science work.
TensorFlow and PyTorch are the dominant libraries for deep learning in Python.
Python is consistently ranked as one of the most popular programming languages in the world.
""".strip()

def fixed_size_chunks(text, chunk_size=200):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def sentence_chunks(text, n=3):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    return [". ".join(sentences[i:i+n]) + "." for i in range(0, len(sentences), n)]

def overlapping_chunks(text, n=3, overlap=1):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    step = n - overlap
    chunks = []
    for i in range(0, len(sentences), step):
        group = sentences[i:i + n]
        if group:
            chunks.append(". ".join(group) + ".")
    return chunks

def build_rag(chunks, collection_name):
    client = chromadb.Client()
    collection = client.create_collection(collection_name)
    embeddings = embed_model.encode(chunks).tolist()
    ids = [f"c_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    return collection

def rag_answer(question, collection):
    results = collection.query(
        query_embeddings=embed_model.encode([question]).tolist(),
        n_results=3,
    )
    chunks = results["documents"][0]
    context = "\n\n".join(f"- {c}" for c in chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    return llm.generate_content(prompt).text.strip(), chunks

strategies = {
    "fixed_size": fixed_size_chunks(document, chunk_size=200),
    "sentence_chunks": sentence_chunks(document, n=3),
    "overlapping_chunks": overlapping_chunks(document, n=3, overlap=1),
}

question = "What libraries are used for deep learning in Python?"

print(f"Question: {question}\n")
print("=" * 60)

for strategy_name, chunks in strategies.items():
    

    collection = build_rag(chunks, strategy_name)
    #collection = build_rag(chunks, strategy_name.replace(" ", "_")[:30])
    answer, used_chunks = rag_answer(question, collection)

    print(f"\nStrategy: {strategy_name} ({len(chunks)} chunks)")
    print(f"Answer: {answer}")
    print(f"Top retrieved chunk: {used_chunks[0][:120]}...")
    print("-" * 60)
