from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
"The cat sat on the mat.",
"A feline rested on the rug.",
"She is learning to code in Python.",
"He is studying programming with Python.",
"The restaurant was fully booked.",
"There were no tables available at the diner.",
"Climate change is accelerating.",
"Global warming is getting worse.",
"He went for a run in the park.",
"She jogged through the garden.",
"The flight was delayed by two hours.",
"The plane departed late.",
"Inflation is rising across the country.",
"Prices are going up everywhere.",
"The movie was boring and too long.",
"The film dragged on and was dull.",
"She plays football on weekends.",
"He enjoys a game of soccer on Saturdays.",
"The hospital was understaffed.",
"There were not enough doctors on duty.",
]

embeddings = model.encode(sentences)
similarity_matrix = cosine_similarity(embeddings)

np.fill_diagonal(similarity_matrix,0)

pairs = []

for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        pairs.append((similarity_matrix[i][j],i,j))

pairs.sort(reverse=True)

print("Top 3 most similar pairs:\n")
for score, i, j in pairs[:3]:
    print(f"Score: {score:.3f}")
    print(f" A: {sentences[i]}")
    print(f" B: {sentences[j]}")    
    print()