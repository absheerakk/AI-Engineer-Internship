def overlapping_chunks(text, sentences_per_chunk=3, overlap=1):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    chunks = []
    step = sentences_per_chunk - overlap
    for i in range(0, len(sentences), step):
        group = sentences[i:i + sentences_per_chunk]
        if group:
            chunks.append(". ".join(group) + ".")
    return chunks

text = """
Python was created by Guido van Rossum and first released in 1991.
It is an interpreted, high-level, general-purpose programming language.
Python's design philosophy emphasises code readability and simplicity.
It supports multiple programming paradigms including procedural, object-oriented, and functional programming.
Python has a large standard library and an active community.
It is widely used in web development, data science, machine learning, and automation.
""".strip()

chunks = overlapping_chunks(text, sentences_per_chunk=3, overlap=1)

print(f"Overlapping chunks (3 sentences, overlap=1) → {len(chunks)} chunks\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i} ---")
    print(chunk)
    print()
