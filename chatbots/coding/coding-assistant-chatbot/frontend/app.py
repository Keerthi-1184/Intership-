import streamlit as st
import requests

st.set_page_config(page_title="Coding Assistant", page_icon="🤖", layout="wide")
st.title("💻 Coding Assistant Chatbot")

# Session state for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Model selector
model = st.selectbox("Choose a Model", [
    "deepseek-r1:1.5b",
    "qwen2.5-coder:0.5b",
    "llama3.2-vision:11b"
])

# Input box
user_input = st.chat_input("Ask your coding question...")

# Display chat history
for entry in st.session_state.chat:
    with st.chat_message("user"):
        st.markdown(entry["user"])
    with st.chat_message("assistant"):
        st.markdown(entry["bot"])

# When user sends a message
if user_input:
    st.session_state.chat.append({"user": user_input, "bot": "..."})
    with st.spinner("Thinking..."):
        res = requests.post(
            "http://localhost:8000/chat",
            json={"prompt": user_input, "model": model}
        )
        reply = res.json().get("response", "Error: No response.")
        st.session_state.chat[-1]["bot"] = reply
        st.rerun()
