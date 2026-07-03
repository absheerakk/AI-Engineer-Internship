import streamlit as st
import time

st.title("Re-render Demo")
st.write(f"Page rendered at: {time.strftime('%H:%M:%S')}")

user_input = st.text_input("Type anything:")

if user_input:
    st.write(f"You typed: {user_input}")

if st.button("Click me"):
    st.write("Button was clicked.")
