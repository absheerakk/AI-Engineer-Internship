import streamlit as st

st.title("File Upload Demo")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.success(f"File uploaded: {uploaded_file.name} ({len(content)} characters)")
    st.text_area("File contents", content, height=300)
else:
    st.info("Upload a .txt file to see its contents.")
