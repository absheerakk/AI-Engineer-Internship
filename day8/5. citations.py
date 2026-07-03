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

def sentence_chunks(text, n=3):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    return [". ".join(sentences[i:i+n]) + "." for i in range(0, len(sentences), n)]

chunks = sentence_chunks(document)
client = chromadb.Client()
collection = client.create_collection("cited_rag")
collection.add(
    documents=chunks,
    embeddings=embed_model.encode(chunks).tolist(),
    ids=[f"c_{i}" for i in range(len(chunks))],
)

def rag_with_citations(question):
    results = collection.query(
        query_embeddings=embed_model.encode([question]).tolist(),
        n_results=3,
    )
    used_chunks = results["documents"][0]
    context = "\n\n".join(f"- {c}" for c in used_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    answer = llm.generate_content(prompt).text.strip()
    return answer, used_chunks

def display(question, answer, sources):
    print(f"Question: {question}")
    print(f"\nAnswer:\n{answer}")
    print(f"\nSources used ({len(sources)}):")
    for i, source in enumerate(sources, 1):
        print(f"  [{i}] {source}")
    print("\n" + "=" * 60 + "\n")

questions = [
    "Who created Python and when?",
    "What is Python used for?",
    "What libraries exist for deep learning?",
    "What is the capital of Pakistan?",
]

for q in questions:
    answer, sources = rag_with_citations(q)
    display(q, answer, sources)
