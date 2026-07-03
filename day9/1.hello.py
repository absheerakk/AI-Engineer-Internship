import streamlit as st

st.title("Hello, Streamlit")
st.write("This is my first web app.")

name = st.text_input("What is your name?")

if name:
    st.success(f"Nice to meet you, {name}!")
