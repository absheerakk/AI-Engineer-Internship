import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("day6_intro")

documents = [
    "The cat sat on the mat.",
    "She is learning to code in Python.",
    "The restaurant had no tables available.",
    "He is studying machine learning.",
    "A feline rested on the rug.",
    "The diner was fully booked.",
]

embeddings = model.encode(documents).tolist()
ids = [f"doc_{i}" for i in range(len(documents))]

collection.add(documents=documents, embeddings=embeddings, ids=ids)

query = "programming and AI"
query_embedding = model.encode([query]).tolist()

results = collection.query(query_embeddings=query_embedding, n_results=3)

print(f"Query: '{query}'\n")
for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"  {1 - distance:.3f}  {doc}")
