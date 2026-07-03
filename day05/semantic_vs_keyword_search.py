from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "The car broke down on the highway.",
    "She adopted a puppy from the shelter.",
    "The automobile engine needs replacing.",
    "He is learning to play the guitar.",
    "The dog was found wandering near the park.",
    "Electric vehicles are becoming more affordable.",
    "She practises piano every evening.",
]

doc_embeddings = model.encode(documents)

def keyword_search(query, docs):
    query_lower = query.lower()
    return [d for d in docs if any(word in d.lower() for word in query_lower.split())]

def semantic_search(query, docs, doc_embeds, top_k=3):
    query_embed = model.encode([query])
    scores = cosine_similarity(query_embed, doc_embeds)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(docs[i], round(scores[i], 3)) for i in top_indices]

queries = [
    "vehicle problems",
    "pets",
    "music",
]

for query in queries:
    print(f"Query: '{query}'")
    print(f"  Keyword results: {keyword_search(query, documents) or 'none'}")
    print(f"  Semantic results:")
    for doc, score in semantic_search(query, documents, doc_embeddings):
        print(f"    {score:.3f}  {doc}")
    print()
