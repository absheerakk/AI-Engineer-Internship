import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("with_metadata")

documents = [
    ("Python is used for machine learning.", "tech"),
    ("Docker simplifies deployment.", "tech"),
    ("Regular exercise improves heart health.", "health"),
    ("Sleep is essential for brain function.", "health"),
    ("A startup needs a clear business model.", "business"),
    ("Customer retention is key to growth.", "business"),
    ("Git tracks changes in your codebase.", "tech"),
    ("A balanced diet supports immune function.", "health"),
]

texts     = [d[0] for d in documents]
metadatas = [{"category": d[1]} for d in documents]
embeddings = model.encode(texts).tolist()
ids = [f"doc_{i}" for i in range(len(texts))]

collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas,
)

query = "staying healthy"
query_embedding = model.encode([query]).tolist()

print(f"Query: '{query}'\n")

print("Without filter (all categories):")
results = collection.query(query_embeddings=query_embedding, n_results=3)
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"  {1 - dist:.3f}  {doc}")

print("\nWith filter (health only):")
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
    where={"category": "health"},
)
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"  {1 - dist:.3f}  {doc}")
