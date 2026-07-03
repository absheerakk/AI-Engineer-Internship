import streamlit as st
import time
from sentence_transformers import SentenceTransformer

st.title("Caching Demo")

# Toggle this decorator on and off to feel the difference
@st.cache_resource
def load_model():
    time.sleep(1)  # simulate a slow load
    return SentenceTransformer("all-MiniLM-L6-v2")

st.write("Loading model...")
model = load_model()
st.success("Model ready.")

text = st.text_input("Enter text to embed:")
if text:
    embedding = model.encode(text)
    st.write(f"Embedding shape: {embedding.shape}")
    st.write(f"First 5 values: {embedding[:5].tolist()}")