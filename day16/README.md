# Day 16 — Capstone Day 2: Build the Core

Today, I built the core terminal-based RAG pipeline for the Capstone project (**Cohort IQ**).

## Key Work Completed
1. **Core Pipeline (`core.py`):** Configured document loading, paragraph-based chunking, embedding generation using `SentenceTransformer`, and retrieval using a persistent ChromaDB database.
2. **Metadata-Based Range Filters:** Improved Chroma retrieval to automatically detect when a user asks about multiple days or topic ranges (e.g., "Compare Day 5 and Day 10" or "between chunking and deployment") and perform multi-day or round-robin queries to prevent retrieval dilution.
3. **Grounded Synthesis:** Integrated the Gemini API using a hardened system prompt ensuring responses are factual, cited, and free of inline brackets.

## Code Location
All actual source code files for the Capstone project (**Cohort IQ**) are managed in a standalone repository and linked directly to this workspace:
* **Standalone Repository:** [CohortIQ](https://github.com/absheerakk/CohortIQ)
* **Local Submodule Path:** Linked as a Git submodule inside the `day15/` directory.