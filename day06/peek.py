import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("inspection_demo")

documents = [
    ("Machine learning is a subfield of AI.", {"topic": "ai", "level": "intro"}),
    ("Gradient descent optimises neural networks.", {"topic": "ai", "level": "advanced"}),
    ("Karachi has a population of over 14 million.", {"topic": "geography", "level": "intro"}),
    ("The Indus Valley Civilisation is one of the oldest.", {"topic": "history", "level": "intro"}),
    ("Transformers use self-attention mechanisms.", {"topic": "ai", "level": "advanced"}),
]

texts     = [d[0] for d in documents]
metadatas = [d[1] for d in documents]
embeddings = model.encode(texts).tolist()
ids = [f"doc_{i}" for i in range(len(texts))]

collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

# How many documents?
print(f"Total documents: {collection.count()}\n")

# Peek at the first 3
peek = collection.peek(limit=3)
print("First 3 documents:")
for doc_id, doc, meta in zip(peek["ids"], peek["documents"], peek["metadatas"]):
    print(f"  [{doc_id}] {meta}  |  {doc}")

print()

# Query with two filters
print("Advanced AI documents only:")
results = collection.query(
    query_embeddings=model.encode(["how do neural networks learn"]).tolist(),
    n_results=5,
    where={"$and": [{"topic": "ai"}, {"level": "advanced"}]},
)
for doc in results["documents"][0]:
    print(f"  {doc}")
