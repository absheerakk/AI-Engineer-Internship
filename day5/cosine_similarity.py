from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity 

model = SentenceTransformer("all-MiniLM-L6-v2")

pairs = [
    ("I love dogs.", "I adore puppies."),
    ("I love dogs.", "The stock market crashed."),
    ("Python is a programming language.", "I use Python to write code."),
    ("Python is a programming language.", "The snake slithered through the grass."),
    ("She is happy.", "She is sad."),
]

for a, b in pairs:
    vec_a = model.encode([a])
    vec_b = model.encode([b])
    score = cosine_similarity(vec_a, vec_b)[0][0]
    print(f"{score:.3f}  |  '{a}'  vs  '{b}'")
