import chromadb
from sentence_transformers import SentenceTransformer

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
"""

def chunk_text(text, chunk_size=2):
    sentences = [s.strip() for s in text.strip().split(".") if s.strip()]
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = ". ".join(sentences[i:i + chunk_size]) + "."
        chunks.append(chunk)
    return chunks

chunks = chunk_text(document, chunk_size=2)
print(f"Created {len(chunks)} chunks:\n")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk}")
print()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("python_facts")

embeddings = model.encode(chunks).tolist()
ids = [f"chunk_{i}" for i in range(len(chunks))]

collection.add(documents=chunks, embeddings=embeddings, ids=ids)
print(f"Stored {collection.count()} chunks in Chroma.\n")


def retrieve(question, collection, model, top_k=3):
    query_embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0]

questions = [
    "When was Python created?",
    "What is Python used for?",
    "What libraries are used for deep learning?",
]

for question in questions:
    print(f"Question: {question}")
    chunks_found = retrieve(question, collection, model)
    for i, chunk in enumerate(chunks_found, 1):
        print(f"  [{i}] {chunk}")
    print()
