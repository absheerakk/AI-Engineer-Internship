import time 
from sentence_transformers  import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [f"This is sentence number {i}." for i in range(100)]

start = time.time()

for s in sentences:
    model.encode(s)
loop_time = round(time.time() - start,3)

start = time.time()
model.encode(sentences)
batch_time = round(time.time() - start, 3)

print(f"Loop: {loop_time}s")
print(f"Batch: {batch_time}s")
print(f"Batch is {round(loop_time/batch_time)}x faster")