import os
import streamlit as st
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@st.cache_resource
def load_embed_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_llm():
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "Answer using only the context provided. "
            "If the answer is not in the context, say 'I don't have that information.'"
        ),
    )

def overlapping_chunks(text, n=3, overlap=1):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    step = n - overlap
    chunks = []
    for i in range(0, len(sentences), step):
        group = sentences[i:i + n]
        if group:
            chunks.append(". ".join(group) + ".")
    return chunks

def build_collection(text, embed_model):
    chunks = overlapping_chunks(text)
    client = chromadb.Client()

    try:
        client.delete_collection("rag_collection")
    except:
        pass

    collection = client.create_collection("rag_collection")
    embeddings = embed_model.encode(chunks).tolist()
    ids = [f"c_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    return collection, len(chunks)

def ask(question, collection, embed_model, llm):
    results = collection.query(
        query_embeddings=embed_model.encode([question]).tolist(),
        n_results=3,
    )
    used_chunks = results["documents"][0]
    context = "\n\n".join(f"- {c}" for c in used_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    answer = llm.generate_content(prompt).text.strip()
    return answer, used_chunks

# ── UI ────────────────────────────────────────────────────────────

embed_model = load_embed_model()
llm = load_llm()

st.title("Document Q&A")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    with st.expander("Document preview"):
        st.text(text[:500] + "..." if len(text) > 500 else text)

    
    try:
        with st.spinner("Indexing document..."):
            collection, chunk_count = build_collection(text, embed_model)
        if chunk_count < 3:
            st.warning("This document is very short. Results may be limited.")
        st.success(f"Indexed {chunk_count} chunks from {uploaded_file.name}")
    except Exception as e:
        st.error(f"Failed to index document: {e}")
        st.stop()


    question = st.text_input(
        "Ask a question about the document:",
        disabled=uploaded_file is None,
        placeholder="Upload a document first..." if uploaded_file is None else "Type your question...",
    )


    if question:
        with st.spinner("Thinking..."):
            answer, sources = ask(question, collection, embed_model, llm)

        st.markdown("### Answer")
        st.write(answer)

        st.markdown("### Sources")
        for i, source in enumerate(sources, 1):
            st.markdown(f"**[{i}]** {source}")

else:
    st.info("Upload a document to get started.")
