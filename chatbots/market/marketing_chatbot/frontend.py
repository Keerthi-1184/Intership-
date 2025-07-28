import streamlit as st
import requests
from urllib.parse import urljoin
import logging
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BACKEND_URL = "http://localhost:8000"
TIMEOUT_SECONDS = 60

# Custom CSS
st.markdown("""
    <style>
        .stTextArea textarea {
            min-height: 150px;
        }
        .stButton button {
            width: 100%;
            transition: all 0.2s;
        }
        .stButton button:hover {
            transform: scale(1.02);
        }
        .chat-message {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .user-message {
            background-color: #f0f2f6;
        }
        .assistant-message {
            background-color: #e6f7ff;
        }
        .stTabs {
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("Marketing Content Generator")
st.markdown("Generate marketing content, analyze images, or create marketing code!")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Backend connection check
def check_backend_connection():
    health_url = urljoin(BACKEND_URL, "/health")
    try:
        response = requests.get(health_url, timeout=5)
        data = response.json()
        logger.info(f"Health check: {data}")
        return response.status_code == 200 and data.get("status") == "ready"
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection error: {str(e)}")
        return False

# Display connection status
if not check_backend_connection():
    st.error(f"""
    Cannot connect to backend at {BACKEND_URL}. Please ensure:
    1. The backend server is running (run `python app.py`)
    2. The marketing_data directory contains text files
    3. Ollama is running with deepseek-r1:1.5b, mxbai-embed-large:latest, llama3.2-vision:11b, and qwen2.5-coder:0.5b
    """)
    if st.button("Retry Connection"):
        st.rerun()
    st.stop()

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Text Generation", "Image Analysis", "Code Generation"])

# Text Generation Tab
with tab1:
    with st.form("text_form"):
        prompt = st.text_area(
            "Enter your marketing prompt (e.g., 'Create a slogan for a coffee brand')",
            placeholder="Type your marketing content request here...",
            key="text_prompt"
        )
        submit_button = st.form_submit_button("Generate", type="primary")

    if submit_button and prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Generating content..."):
            try:
                response = requests.post(
                    urljoin(BACKEND_URL, "/query"),
                    json={"question": prompt},
                    timeout=TIMEOUT_SECONDS
                )
                response.raise_for_status()
                data = response.json()

                assistant_response = data.get("response", "No response received")
                sources = data.get("sources", [])
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response,
                    "sources": sources
                })

            except requests.exceptions.Timeout:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Request timed out. Please try again."
                })
            except requests.exceptions.RequestException as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Connection error: {str(e)}"
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })
        
        st.rerun()

# Image Analysis Tab
with tab2:
    with st.form("image_form"):
        uploaded_file = st.file_uploader("Upload an image for marketing analysis", type=["png", "jpg", "jpeg"])
        image_submit = st.form_submit_button("Analyze Image", type="primary")

    if image_submit and uploaded_file:
        with st.spinner("Analyzing image..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(
                    urljoin(BACKEND_URL, "/image_analysis"),
                    files=files,
                    timeout=TIMEOUT_SECONDS
                )
                response.raise_for_status()
                data = response.json()

                st.session_state.messages.append({
                    "role": "user",
                    "content": f"Uploaded image: {uploaded_file.name}"
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data.get("response", "No response received")
                })

            except requests.exceptions.Timeout:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Request timed out. Please try again."
                })
            except requests.exceptions.RequestException as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Connection error: {str(e)}"
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })
        
        st.rerun()

# Code Generation Tab
with tab3:
    with st.form("code_form"):
        code_prompt = st.text_area(
            "Enter your code prompt (e.g., 'Generate HTML for an email campaign')",
            placeholder="Type your marketing code request here...",
            key="code_prompt"
        )
        code_submit = st.form_submit_button("Generate Code", type="primary")

    if code_submit and code_prompt.strip():
        st.session_state.messages.append({"role": "user", "content": code_prompt})
        
        with st.spinner("Generating code..."):
            try:
                response = requests.post(
                    urljoin(BACKEND_URL, "/code_generation"),
                    json={"question": code_prompt},
                    timeout=TIMEOUT_SECONDS
                )
                response.raise_for_status()
                data = response.json()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data.get("response", "No response received")
                })

            except requests.exceptions.Timeout:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Request timed out. Please try again."
                })
            except requests.exceptions.RequestException as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Connection error: {str(e)}"
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })
        
        st.rerun()

# Display chat history
with st.container():
    for message in st.session_state.messages:
        message_class = "user-message" if message["role"] == "user" else "assistant-message"
        st.markdown(
            f'<div class="chat-message {message_class}">'
            f'<strong>{message["role"].title()}:</strong> {message["content"]}'
            '</div>',
            unsafe_allow_html=True
        )
        if message.get("sources"):
            with st.expander("View Sources"):
                for src in message["sources"]:
                    st.code(src.split("/")[-1], language="text")

# Clear chat button
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()