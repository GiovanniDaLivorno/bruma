import streamlit as st
from openai import OpenAI

# Define your system prompt
SYSTEM_PROMPT = "You are Bruma, a helpful assistant. Answer concisely and never repeat yourself."

# Key point: Use Docker service name, not localhost
client = OpenAI(
    base_url="http://bruma-ie:8080/v1",
    api_key="not-needed"  # bruma-ie has no API key set
)

st.title("Bruma · Qwen 1.5B")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input and streaming response
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="qwen",  # Fill in anything; llama-server only loads one model
            messages=st.session_state.messages,
            stream=True,
            max_tokens=256
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
