# import streamlit as st
# import requests

# st.set_page_config(page_title="Customer Support Assistant", page_icon="📞", layout="wide")
# st.title("🛠️ Customer Support Chatbot")

# # Session state
# if "chat" not in st.session_state:
#     st.session_state.chat = []

# # Model selector
# model = st.selectbox("Choose a Model", [
#     "deepseek-r1:1.5b",
#     "qwen2.5-coder:0.5b",
#     "llama3.2-vision:11b"
# ])

# # Chat input
# user_input = st.chat_input("Describe your issue or ask a question...")

# # Chat history
# for entry in st.session_state.chat:
#     with st.chat_message("user"):
#         st.markdown(entry["user"])
#     with st.chat_message("assistant"):
#         st.markdown(entry["bot"])

# # Handle input
# if user_input:
#     st.session_state.chat.append({"user": user_input, "bot": "..."})
#     with st.spinner("Please wait..."):
#         res = requests.post(
#             "http://localhost:8000/chat",
#             json={"prompt": user_input, "model": model}
#         )
#         reply = res.json().get("response", "Error: No response.")
#         st.session_state.chat[-1]["bot"] = reply
#         st.rerun()


import streamlit as st
import requests
from streamlit.components.v1 import html

st.set_page_config(page_title="Customer Support Assistant", layout="wide")

# Custom CSS for background and styling
st.markdown("""
    <style>
        /* Background image */
        body {
            background-image: url('https://images.unsplash.com/photo-1521791136064-7986c2920216');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* Glassmorphism chat container */
        .chat-container {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(12px);
            color: #fff;
        }

        /* Chat bubbles */
        .bubble-user, .bubble-bot {
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            max-width: 85%;
        }
        .bubble-user {
            background-color: rgba(30, 144, 255, 0.6);
            align-self: flex-end;
        }
        .bubble-bot {
            background-color: rgba(255, 255, 255, 0.3);
        }

        .avatar {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📞 Customer Support Chatbot")

# Model Selector with badges
model = st.selectbox("Choose Support Mode", [
    "deepseek-r1:1.5b 🧠 General Assistant",
    "qwen2.5-coder:0.5b 🔧 Tech Support",
    "llama3.2-vision:11b 🖼️ Visual Support"
])

# Model name for API
model_key = model.split(" ")[0]

# Initialize chat state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for entry in st.session_state.chat:
        st.markdown(f"""
            <div style="display: flex; flex-direction: row; justify-content: flex-end;">
                <div class="bubble-user">{entry['user']}</div>
            </div>
            <div style="display: flex; flex-direction: row;">
                <img src="https://img.icons8.com/ios-filled/50/customer-support.png" class="avatar"/>
                <div class="bubble-bot">{entry['bot']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Input box
user_input = st.chat_input("How can I help you today?")

if user_input:
    st.session_state.chat.append({"user": user_input, "bot": "..."})
    with st.spinner("Let me check that for you..."):
        res = requests.post(
            "http://localhost:8000/chat",
            json={"prompt": user_input, "model": model_key}
        )
        reply = res.json().get("response", "⚠️ Sorry, something went wrong.")
        st.session_state.chat[-1]["bot"] = reply
        st.rerun()
