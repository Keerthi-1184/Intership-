
# import streamlit as st
# import requests
# from io import BytesIO
# import time

# # Streamlit app
# st.title("Voice Chatbot")

# # Input form
# with st.form(key="chatbot_form"):
#     text_input = st.text_input("Text Input (optional)", placeholder="Enter your query")
#     audio_file = st.file_uploader("Audio Input (optional)", type=["wav"])
#     target_language = st.selectbox("Target Language", ["english", "spanish", "french", "german", "hindi"])
#     model_name = st.text_input("Model Name", value="deepseek-r1:1.5b")
#     submit_button = st.form_submit_button("Submit")

# # Initialize session state
# if "response" not in st.session_state:
#     st.session_state.response = None
# if "error" not in st.session_state:
#     st.session_state.error = None
# if "audio_url" not in st.session_state:
#     st.session_state.audio_url = None
# if "debug_info" not in st.session_state:
#     st.session_state.debug_info = None
# if "backend_version" not in st.session_state:
#     st.session_state.backend_version = None

# if submit_button:
#     # Reset session state
#     st.session_state.response = None
#     st.session_state.error = None
#     st.session_state.audio_url = None
#     st.session_state.debug_info = None
#     st.session_state.backend_version = None

#     # Prepare form data
#     data = {
#         "target_language": target_language,
#         "model_name": model_name,
#     }
#     files = {}
#     if text_input:
#         data["text"] = text_input
#     if audio_file:
#         files["audio"] = (audio_file.name, audio_file, "audio/wav")

#     try:
#         st.write("Sending request to backend...")
#         start_time = time.time()
#         response = requests.post(
#             "http://localhost:8000/process",
#             data=data,
#             files=files if files else None,
#             timeout=90,
#         )
#         elapsed_time = time.time() - start_time
#         response.raise_for_status()

#         result = response.json()
#         st.session_state.debug_info = f"Backend response (took {elapsed_time:.2f}s): {result}"
#         st.session_state.response = result.get("response", "No response received")
#         st.session_state.audio_url = result.get("audio_url", "")
#         st.session_state.error = result.get("error", "")
#         st.session_state.backend_version = result.get("version", "Unknown")

#         # Check for unexpected audio_path
#         if "audio_path" in result:
#             st.session_state.error = "Backend returned 'audio_path' instead of 'audio_url'. Please update main.py to the latest version."
#         # Check backend version
#         if st.session_state.backend_version != "2025-05-22":
#             st.session_state.error = f"Backend version is {st.session_state.backend_version}. Expected 2025-05-22. Please update main.py."

#     except requests.exceptions.Timeout:
#         st.session_state.error = "Request timed out after 90 seconds. Try a simpler query or check backend performance."
#         st.session_state.debug_info = "Timeout occurred"
#     except requests.exceptions.ConnectionError as e:
#         st.session_state.error = f"Cannot connect to backend: {str(e)}. Ensure the backend is running on http://localhost:8000."
#         st.session_state.debug_info = "Connection error"
#     except requests.exceptions.HTTPError as e:
#         st.session_state.error = f"HTTP error: {str(e)}"
#         st.session_state.debug_info = f"HTTP error: {e.response.text}"
#     except Exception as e:
#         st.session_state.error = f"Unexpected error: {str(e)}"
#         st.session_state.debug_info = "Unexpected error"

# # Display results only if available


# if st.session_state.backend_version:
#     st.write(f"**Backend Version:** {st.session_state.backend_version}")

# if st.session_state.error:
#     st.error(f"**Error:** {st.session_state.error}")

# if st.session_state.response:
#     st.write("**Response:**")
#     st.write(st.session_state.response)

# if st.session_state.audio_url:
#     try:
#         full_audio_url = f"http://localhost:8000{st.session_state.audio_url}"
#         st.write(f"**Audio URL:** {full_audio_url}")
#         audio_response = requests.get(full_audio_url, timeout=10)
#         audio_response.raise_for_status()
#         audio_bytes = BytesIO(audio_response.content)
#         st.audio(audio_bytes, format="audio/mp3")
#         # Provide a download link as a fallback
#         st.download_button(
#             label="Download Audio",
#             data=audio_bytes,
#             file_name="output_audio.mp3",
#             mime="audio/mp3",
#         )
#     except Exception as e:
#         st.error(f"Error fetching or playing audio: {str(e)}")
#         st.write("No audio received")
# elif st.session_state.response or st.session_state.error:
#     st.write("No audio received")

import streamlit as st
import requests
from io import BytesIO
import time
from streamlit_mic_recorder import mic_recorder

# Streamlit app
st.title("Voice Chatbot")

# Input form
with st.form(key="chatbot_form"):
    text_input = st.text_input("Text Input (optional)", placeholder="Enter your query")
    audio_file = st.file_uploader("Audio Input (optional)", type=["wav"])
    st.write("Record Audio (optional):")
    recorded_audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="🛑 Stop Recording",
        key="mic_recorder",
        format="wav"
    )
    target_language = st.selectbox("Target Language", ["english", "spanish", "french", "german", "hindi"])
    model_name = st.text_input("Model Name", value="deepseek-r1:1.5b")
    submit_button = st.form_submit_button("Submit")

# Initialize session state
if "query" not in st.session_state:
    st.session_state.query = None
if "response" not in st.session_state:
    st.session_state.response = None
if "error" not in st.session_state:
    st.session_state.error = None
if "audio_url" not in st.session_state:
    st.session_state.audio_url = None
if "debug_info" not in st.session_state:
    st.session_state.debug_info = None
if "backend_version" not in st.session_state:
    st.session_state.backend_version = None

if submit_button:
    # Reset session state
    st.session_state.query = None
    st.session_state.response = None
    st.session_state.error = None
    st.session_state.audio_url = None
    st.session_state.debug_info = None
    st.session_state.backend_version = None

    # Prepare form data
    data = {
        "target_language": target_language,
        "model_name": model_name,
    }
    files = {}
    if text_input:
        data["text"] = text_input
    elif audio_file:
        files["audio"] = (audio_file.name, audio_file, "audio/wav")
    elif recorded_audio and recorded_audio.get("bytes"):
        try:
            audio_bytes = recorded_audio["bytes"]
            if not audio_bytes:
                raise ValueError("No audio data recorded")
            files["audio"] = ("recorded_audio.wav", BytesIO(audio_bytes), "audio/wav")
        except Exception as e:
            st.session_state.error = f"Error processing recorded audio: {str(e)}"
            st.session_state.debug_info = "Recorded audio processing failed"

    if not (text_input or audio_file or (recorded_audio and recorded_audio.get("bytes"))):
        st.session_state.error = "Please provide text, an audio file, or record audio."
        st.session_state.debug_info = "No input provided"

    if files or text_input:
        try:
            st.write("Sending request to backend...")
            start_time = time.time()
            response = requests.post(
                "http://localhost:8000/process",
                data=data,
                files=files if files else None,
                timeout=90,
            )
            elapsed_time = time.time() - start_time
            response.raise_for_status()

            result = response.json()
            st.session_state.debug_info = f"Backend response (took {elapsed_time:.2f}s): {result}"
            st.session_state.query = result.get("query", None)
            st.session_state.response = result.get("response", "No response received")
            st.session_state.audio_url = result.get("audio_url", "")
            st.session_state.error = result.get("error", "")
            st.session_state.backend_version = result.get("version", "Unknown")

            # Check for unexpected audio_path
            if "audio_path" in result:
                st.session_state.error = "Backend returned 'audio_path' instead of 'audio_url'. Please update main.py to the latest version."
            # Check backend version
            if st.session_state.backend_version != "2025-05-22":
                st.session_state.error = f"Backend version is {st.session_state.backend_version}. Expected 2025-05-22. Please update main.py."
            # Check for transcription or model errors
            if st.session_state.error or "Error" in st.session_state.response:
                st.session_state.error = st.session_state.error or st.session_state.response

        except requests.exceptions.Timeout:
            st.session_state.error = "Request timed out after 90 seconds. Try a simpler query or check backend performance."
            st.session_state.debug_info = "Timeout occurred"
        except requests.exceptions.ConnectionError as e:
            st.session_state.error = f"Cannot connect to backend: {str(e)}. Ensure the backend is running on http://localhost:8000."
            st.session_state.debug_info = "Connection error"
        except requests.exceptions.HTTPError as e:
            st.session_state.error = f"HTTP error: {str(e)}"
            st.session_state.debug_info = f"HTTP error: {e.response.text}"
        except Exception as e:
            st.session_state.error = f"Unexpected error: {str(e)}"
            st.session_state.debug_info = "Unexpected error"

# Display results only if available
if st.session_state.debug_info:
    st.write(f"**Debug Info:** {st.session_state.debug_info}")

if st.session_state.backend_version:
    st.write(f"**Backend Version:** {st.session_state.backend_version}")

if st.session_state.error:
    st.error(f"**Error:** {st.session_state.error}")

if st.session_state.query and not st.session_state.error:
    st.write("**Your Query:**")
    st.write(st.session_state.query)

if st.session_state.response:
    st.write("**Response:**")
    st.write(st.session_state.response)

if st.session_state.audio_url:
    try:
        full_audio_url = f"http://localhost:8000{st.session_state.audio_url}"
        st.write(f"**Audio URL:** {full_audio_url}")
        audio_response = requests.get(full_audio_url, timeout=10)
        audio_response.raise_for_status()
        audio_bytes = BytesIO(audio_response.content)
        st.audio(audio_bytes, format="audio/mp3")
        # Provide a download link as a fallback
        st.download_button(
            label="Download Audio",
            data=audio_bytes,
            file_name="output_audio.mp3",
            mime="audio/mp3",
        )
    except Exception as e:
        st.error(f"Error fetching or playing audio: {str(e)}")
        st.write("No audio received")
elif st.session_state.response or st.session_state.error:
    st.write("No audio received")