# import streamlit as st
# import requests
# import time
# from urllib.parse import urljoin

# # Configuration
# BACKEND_URL = "http://localhost:8000"  # Update if your backend runs elsewhere
# TIMEOUT_SECONDS = 600

# # Custom CSS for better styling
# st.markdown("""
#     <style>
#         .stTextArea textarea {
#             min-height: 150px;
#         }
#         .stButton button {
#             width: 100%;
#             transition: all 0.2s;
#         }
#         .stButton button:hover {
#             transform: scale(1.02);
#         }
#         .chat-message {
#             padding: 12px;
#             border-radius: 8px;
#             margin-bottom: 12px;
#         }
#         .user-message {
#             background-color: #f0f2f6;
#         }
#         .assistant-message {
#             background-color: #e6f7ff;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # App Title
# st.title("VSoft Consulting Chatbot")
# st.markdown("Ask me anything about VSoft's services and solutions")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Backend connection check with retries
# def check_backend_connection():
#     health_url = urljoin(BACKEND_URL, "/health")
#     try:
#         response = requests.get(health_url, timeout=5)
#         return response.status_code == 200
#     except requests.exceptions.RequestException as e:
#         st.error(f"Connection error: {str(e)}")
#         return False

# # Display connection status
# if not check_backend_connection():
#     st.error(f"""
#     Cannot connect to backend at {BACKEND_URL}. Please ensure:
#     1. The backend server is running (check terminal)
#     2. The URL is correct
#     3. No firewall is blocking the connection
#     """)
#     if st.button("Retry Connection"):
#         st.rerun()
#     st.stop()

# # Chat interface
# with st.container():
#     # Display chat messages
#     for message in st.session_state.messages:
#         message_class = "user-message" if message["role"] == "user" else "assistant-message"
#         st.markdown(
#             f'<div class="chat-message {message_class}">'
#             f'<strong>{message["role"].title()}:</strong> {message["content"]}'
#             '</div>',
#             unsafe_allow_html=True
#         )
        
#         if message.get("sources"):
#             with st.expander("View Sources"):
#                 for src in message["sources"]:
#                     st.code(src.split("/")[-1], language="text")

# # User input area
# with st.form("chat_form"):
#     prompt = st.text_area(
#         "Your message:",
#         placeholder="Type your question about VSoft here...",
#         key="prompt_input"
#     )
    
#     submit_button = st.form_submit_button("Send", type="primary")

# # Handle form submission
# if submit_button and prompt.strip():
#     # Add user message to history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.rerun()  # Refresh to show user message immediately

#     # Prepare for assistant response
#     with st.spinner("Thinking..."):
#         try:
#             # Call backend API
#             response = requests.post(
#                 urljoin(BACKEND_URL, "/query"),
#                 json={"question": prompt},
#                 timeout=TIMEOUT_SECONDS
#             )
#             response.raise_for_status()
#             print("Backend raw response:", response.text)
#             data = response.json()

#             # Stream the response
#             assistant_response = data.get("response", "No response received")
#             sources = data.get("sources", [])
            
#             # Add assistant response to history
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": assistant_response,
#                 "sources": sources
#             })

#         except requests.exceptions.Timeout:
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": "Request timed out. Please try again."
#             })
#         except requests.exceptions.RequestException as e:
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": f"Connection error: {str(e)}"
#             })
#         except Exception as e:
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": f"Error: {str(e)}"
#             })
    
#     st.rerun()  # Refresh to show assistant response

# # Clear chat button
# if st.button("Clear Conversation"):
#     st.session_state.messages = []
#     st.rerun()


import streamlit as st
import requests
from urllib.parse import urljoin
import logging

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
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("VSoft Consulting Chatbot")
st.markdown("Ask me anything about VSoft's services and solutions")

# Initialize chat history
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
    2. The vsoft_data directory contains HTML files
    3. Ollama is running with the deepseek-r1:1.5b model
    """)
    if st.button("Retry Connection"):
        st.rerun()
    st.stop()

# Chat interface
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

# User input area
with st.form("chat_form"):
    prompt = st.text_area(
        "Your message:",
        placeholder="Type your question about VSoft here...",
        key="prompt_input"
    )
    submit_button = st.form_submit_button("Send", type="primary")

# Handle form submission
if submit_button and prompt.strip():
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                urljoin(BACKEND_URL, "/query"),
                json={"question": prompt},
                timeout=TIMEOUT_SECONDS
            )
            response.raise_for_status()
            logger.info(f"Backend response: {response.text}")
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

# Clear chat button
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()