from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
"I enjoy hiking in the mountains.",
"Trail running is my favourite weekend activity.",
"The neural network has three hidden layers.",
"Camping under the stars is deeply relaxing.",
"She loves outdoor adventures.",
]

embeddings = model.encode(sentences)
similarity_matrix = cosine_similarity(embeddings)

avg_similarities = similarity_matrix.mean(axis=1)

odd_one_out = sentences[np.argmin(avg_similarities)]
print("Odd one out:  ", odd_one_out)
print()

for sentence, score in zip(sentences, avg_similarities):
    print(f"{score:.3f} {sentence}")
                                                                 