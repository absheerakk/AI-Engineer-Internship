from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
"I love dogs.",
"I adore puppies.",
"The stock market crashed today.",
"Python is a programming language.",
"She has a pet cat.",
]

embeddings = model.encode(sentences)

for sentence, vector in zip(sentences, embeddings):
    preview = ",".join(f"{x:.3f}" for x in vector[:8])
    print(f"{sentence}")
    print(f"[{preview},...] ({len(vector)} dimensions total)")
    print()
