import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("persistent_demo")

# Only add documents if the collection is empty
if collection.count() == 0:
    print("First run — embedding and storing documents...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    documents = [
        "Python is a high-level programming language.",
        "Machine learning models learn from data.",
        "Karachi is the largest city in Pakistan.",
        "The Gemini API provides access to large language models.",
        "Embeddings represent text as vectors of numbers.",
        "Islamabad is the capital of Pakistan.",
        "Neural networks are inspired by the human brain.",
        "Lahore is known for its rich cultural heritage.",
    ]

    embeddings = model.encode(documents).tolist()
    ids = [f"doc_{i}" for i in range(len(documents))]
    collection.add(documents=documents, embeddings=embeddings, ids=ids)
    print(f"Stored {len(documents)} documents.\n")
else:
    print(f"Loaded existing collection with {collection.count()} documents.\n")
    model = SentenceTransformer("all-MiniLM-L6-v2")

query = "cities in Pakistan"
results = collection.query(
    query_embeddings=model.encode([query]).tolist(),
    n_results=3,
)

print(f"Query: '{query}'\n")
for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"  {1 - distance:.3f}  {doc}")
