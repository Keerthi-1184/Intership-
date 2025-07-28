# (Good Code)
import streamlit as st
import requests
 
st.set_page_config(page_title="Chatbot", layout="centered")
 
# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox("Choose a model:", ["llama3.2-vision:11b", "qwen2.5-coder:0.5b"])
theme_choice = st.sidebar.radio("Select Theme:", ["Light", "Dark"])
 
# --- Theme Styling ---
if theme_choice == "Dark":
    background_color = "#1E1E1E"
    text_color = "#FFFFFF"
    sidebar_bg = "#1E1E1E"
    topbar_bg = "#1E1E1E"
    input_area_bg = "#1E1E1E"
    input_box_bg = "#2C2C2C"
else:
    background_color = "#FFFFFF"
    text_color = "#000000"
    sidebar_bg = "#FFFFFF"
    topbar_bg = "#FFFFFF"
    input_area_bg = "#FFFFFF"
    input_box_bg = "#F9F9F9"
 
# --- Apply Custom Theme CSS ---
st.markdown(
    f"""
    <style>
        .main {{
            background-color: {background_color};
            color: {text_color};
        }}
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
        }}
        header {{
            background-color: {topbar_bg} !important;
        }}
        header div, header span {{
            color: {text_color} !important;
        }}
        section[data-testid="chat-input-container"], div[data-testid="chat-input-container"] {{
            background-color: {input_area_bg} !important;
            padding: 1rem 0.5rem;
            border-top: 1px solid #ccc;
        }}
        section[data-testid="stChatInput"], div[data-testid="stChatInput"] {{
            background-color: {input_area_bg} !important;
        }}
        textarea, input {{
            background-color: {input_box_bg} !important;
            color: {text_color} !important;
        }}
        button {{
            background-color: {input_box_bg} !important;
            color: {text_color} !important;
        }}
        div.stChatMessage {{
            background-color: {'#2c2c2c' if theme_choice == 'Dark' else '#f0f2f6'};
            border-radius: 10px;
            padding: 8px;
        }}
        h1, h2, h3, h4, h5, h6, p, label, span {{
            color: {text_color};
        }}
    </style>
    """,
    unsafe_allow_html=True
)
 
# --- Title ---
st.title("🧠 Aester")
 
# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False
 
# --- Chat History ---
st.markdown("### 💬 Chat History")
for msg in st.session_state.chat_history:
    speaker = "👤 You" if msg["role"] == "user" else "🤖 Bot"
    with st.chat_message(speaker):
        st.markdown(msg["content"])
 
# --- Chat Input ---
if not st.session_state.chat_ended:
    user_input = st.chat_input("Ask me anything (type `exit` to end chat)")
 
    if user_input:
        if user_input.strip().lower() == "exit":
            st.session_state.chat_ended = True
            st.info("💾 Chat session ended. Here's your full conversation:")
 
            full_chat = ""
            for msg in st.session_state.chat_history:
                role = "You" if msg["role"] == "user" else "Bot"
                full_chat += f"{role}: {msg['content']}\n\n"
 
            st.text_area("📄 Chat Session Transcript", full_chat.strip(), height=400)
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("👤 You"):
                st.markdown(user_input)
 
            with st.spinner("🤖 Generating response..."):
                payload = {
                    "model_name": model_choice,
                    "messages": st.session_state.chat_history
                }
 
                try:
                    response = requests.post("http://localhost:8000/chat/", json=payload, timeout=120)
                    if response.status_code == 200:
                        reply = response.json()["response"]
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        with st.chat_message("🤖 Bot"):
                            st.markdown(reply)
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")
 