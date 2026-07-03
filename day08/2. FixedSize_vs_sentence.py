def fixed_size_chunks(text, chunk_size=200):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def sentence_chunks(text, sentences_per_chunk=3):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        group = sentences[i:i + sentences_per_chunk]
        chunks.append(". ".join(group) + ".")
    return chunks

text = """
Python was created by Guido van Rossum and first released in 1991.
It is an interpreted, high-level, general-purpose programming language.
Python's design philosophy emphasises code readability and simplicity.
It supports multiple programming paradigms including procedural, object-oriented, and functional programming.
Python has a large standard library and an active community.
It is widely used in web development, data science, machine learning, and automation.
The name Python comes from the BBC television show Monty Python's Flying Circus.
Python 2 reached end of life in 2020 and Python 3 is the current standard.
Popular Python frameworks include Django and Flask for web development.
NumPy, Pandas, and Scikit-learn are widely used for data science work.
TensorFlow and PyTorch are the dominant libraries for deep learning in Python.
Python is consistently ranked as one of the most popular programming languages in the world.
""".strip()

fixed = fixed_size_chunks(text, chunk_size=200)
sentence = sentence_chunks(text, sentences_per_chunk=3)

print(f"Fixed-size:  {len(fixed)} chunks")
print(f"Sentence:    {len(sentence)} chunks\n")

print("=== Fixed-size ===")
for i, c in enumerate(fixed):
    print(f"[{i}] {repr(c)}\n")

print("=== Sentence ===")
for i, c in enumerate(sentence):
    print(f"[{i}] {c}\n")
