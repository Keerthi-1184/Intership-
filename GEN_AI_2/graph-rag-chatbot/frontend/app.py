import streamlit as st
import requests
import os

st.title("Multilingual Chatbot")

user_input = st.text_input("Ask something:")
language = st.selectbox("Choose Language", ["english", "hindi", "french", "german", "spanish"])
model = st.selectbox("Choose Model", ["deepseek-r1:1.5b", "llama3.2-vision:11b", "qwen2.5-coder:0.5b"])

if st.button("Send") and user_input:
    with st.spinner("Generating response..."):
        response = requests.post("http://localhost:8000/process", json={
            "user_input": user_input,
            "language": language,
            "model": model
        })

        if response.status_code == 200:
            result = response.json()
            st.subheader("🧠 Response:")
            st.write(result["response"])

            audio_path = result.get("audio_path")
            if audio_path and os.path.exists(audio_path):
                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                st.subheader("🔊 Audio Response:")
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.info("Text response ready, but no audio file found.")
        else:
            st.error(f"API Error: {response.status_code}")
