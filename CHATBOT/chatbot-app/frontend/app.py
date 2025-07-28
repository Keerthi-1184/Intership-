import streamlit as st
import requests
import json
import base64
from datetime import datetime

# App config
st.set_page_config(layout="wide", page_title="Multi-Model Chatbot")

# Constants
BACKEND_URL = "http://localhost:8000/chat"
MODELS = {
    "llama3.2-vision:11b": "llama3.2-vision:11b",
    "qwen2.5-coder:0.5b": "qwen2.5-coder:0.5b"
}

# Initialize session state
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_model" not in st.session_state:
        st.session_state.current_model = list(MODELS.keys())[0]
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

init_session_state()

# Helper functions
def display_chat_message(role, content, image=None):
    with st.chat_message(role):
        st.markdown(content)
        if image and role == "user":
            st.image(image, width=300)

def get_image_base64(uploaded_file):
    if uploaded_file:
        return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
    return None

def export_chat_history():
    return json.dumps([
        {"role": msg["role"], "content": msg["content"], "timestamp": msg.get("timestamp", "")}
        for msg in st.session_state.messages
    ], indent=2)

def send_to_backend(payload):
    try:
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code != 200:
            st.error(f"Backend error: {response.text}")
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with backend: {str(e)}")
        return None

# Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.header("Prompt")
    prompt = st.text_area("Enter your prompt:", height=200, key="prompt_input")
    uploaded_file = st.file_uploader("Upload image (optional)", type=["png", "jpg", "jpeg"])

with col2:
    st.header("Chat")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"], message.get("image"))
    
    # Handle new messages
    if prompt or (uploaded_file and st.session_state.get("prompt_input")):
        # Add user message to history
        user_message = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        }
        
        if uploaded_file:
            user_message["image"] = uploaded_file
            st.session_state.uploaded_image = uploaded_file
        
        st.session_state.messages.append(user_message)
        
        # Display user message immediately
        display_chat_message("user", prompt, uploaded_file)
        
        # Prepare API request
        messages_for_api = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
        payload = {
            "model": st.session_state.current_model,
            "messages": messages_for_api,
            "temperature": st.session_state.temperature
        }
        
        if uploaded_file:
            payload["image_url"] = f"data:image/jpeg;base64,{get_image_base64(uploaded_file)}"
        
        # Call backend
        with st.spinner("Generating response..."):
            response = send_to_backend(payload)
            if response:
                bot_response = response.get("message", {}).get("content", "No response generated")
                
                # Add and display assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_response,
                    "timestamp": datetime.now().isoformat()
                })
                display_chat_message("assistant", bot_response)

with col3:
    st.header("Settings")
    
    # Model selection
    st.session_state.current_model = st.selectbox(
        "Select Model:",
        list(MODELS.keys()),
        format_func=lambda x: MODELS[x]
    )
    
    # Temperature
    st.session_state.temperature = st.slider(
        "Temperature:",
        0.0, 1.0, st.session_state.temperature, 0.1
    )
    
    # Theme
    st.session_state.dark_mode = st.toggle("Dark Mode", st.session_state.dark_mode)
    
    # Chat actions
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.uploaded_image = None
        st.rerun()
    
    # Export
    st.download_button(
        "Export Chat",
        export_chat_history(),
        "chat_history.json",
        "application/json"
    )

# Apply theme
if st.session_state.dark_mode:
    st.markdown("""
        <style>
            .stApp { background-color: #1e1e1e; color: white; }
            .stTextInput input, .stTextArea textarea { color: white !important; }
            .stSelectbox select { color: white !important; }
        </style>
    """, unsafe_allow_html=True)