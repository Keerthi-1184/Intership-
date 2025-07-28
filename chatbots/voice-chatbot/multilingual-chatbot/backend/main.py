

# import os
# import uuid
# import logging
# import time
# from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from speech_to_text import transcribe_audio
# from detect_language import detect_language
# from translator import translate_text
# from text_to_speech import text_to_speech
# from chatbot import generate_response

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI()

# # Mount static directory for serving audio files
# app.mount("/static", StaticFiles(directory="static/audio"), name="static")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8501"],  # Streamlit port
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ResponseOutput(BaseModel):
#     response: str
#     audio_url: str
#     error: str | None = None
#     version: str = "2025-05-22"  # Version to verify correct main.py

# @app.post("/process", response_model=ResponseOutput)
# async def process_input(
#     target_language: str = Form(...),
#     model_name: str = Form(...),
#     text: str = Form(None),
#     audio: UploadFile = File(None),
# ):
#     start_time = time.time()
#     logger.info(f"Received request: target_language={target_language}, model_name={model_name}, text={text}, audio={audio.filename if audio else None}")

#     # Create directories
#     os.makedirs("audio", exist_ok=True)
#     os.makedirs("static/audio", exist_ok=True)

#     # Clean up old audio files (older than 1 hour)
#     import glob
#     for old_file in glob.glob("static/audio/output_audio_*.mp3"):
#         if os.path.getmtime(old_file) < time.time() - 3600:
#             os.remove(old_file)
#             logger.info(f"Cleaned up old audio: {old_file}")

#     # Step 1: Get input query
#     audio_path = None
#     try:
#         if audio:
#             audio_path = os.path.join("audio", f"input_audio_{uuid.uuid4()}.wav")
#             with open(audio_path, "wb") as f:
#                 f.write(await audio.read())
#             logger.info(f"Transcribing audio from {audio_path}")
#             query_start = time.time()
#             query = transcribe_audio(audio_path)
#             logger.info(f"Transcription took {time.time() - query_start:.2f}s")
#         else:
#             query = text

#         if not query:
#             raise ValueError("No valid input provided")

#         logger.info(f"Query: {query}")

#         # Step 2: Detect and translate to English if needed
#         detect_start = time.time()
#         detected_lang = detect_language(query)
#         logger.info(f"Detected language: {detected_lang}, took {time.time() - detect_start:.2f}s")
#         if detected_lang != "en":
#             translate_start = time.time()
#             query = translate_text(query, detected_lang, "en")
#             logger.info(f"Translated query to English: {query}, took {time.time() - translate_start:.2f}s")

#         # Step 3: Generate chatbot response
#         chatbot_start = time.time()
#         response = generate_response(query, model_name)
#         logger.info(f"Chatbot response: {response}, took {time.time() - chatbot_start:.2f}s")

#         # Step 4: Translate back to target language if needed
#         if target_language.lower() != "english":
#             translate_back_start = time.time()
#             response = translate_text(response, "en", target_language.lower())
#             logger.info(f"Translated response to {target_language}: {response}, took {time.time() - translate_back_start:.2f}s")

#         # Step 5: Text-to-speech to generate audio
#         audio_output_filename = f"output_audio_{uuid.uuid4()}.mp3"
#         audio_output_path = os.path.join("static/audio", audio_output_filename)
#         logger.info(f"Generating audio at {audio_output_path}")
#         tts_start = time.time()
#         text_to_speech(response, audio_output_path, target_language)
#         logger.info(f"TTS generation took {time.time() - tts_start:.2f}s")

#         # Verify audio file exists
#         if not os.path.exists(audio_output_path):
#             raise RuntimeError("Audio file was not created")

#         # Step 6: Generate audio URL
#         audio_url = f"/static/{audio_output_filename}"
#         logger.info(f"Audio URL: {audio_url}")

#         logger.info(f"Total request time: {time.time() - start_time:.2f}s")
#         return ResponseOutput(response=response, audio_url=audio_url)

#     except Exception as e:
#         logger.error(f"Error processing request: {str(e)}")
#         return ResponseOutput(response="", audio_url="", error=str(e))

#     finally:
#         # Cleanup input audio file
#         if audio_path and os.path.exists(audio_path):
#             try:
#                 os.remove(audio_path)
#                 logger.info(f"Cleaned up input audio: {audio_path}")
#             except Exception as e:
#                 logger.error(f"Failed to clean up {audio_path}: {str(e)}")

import os
import uuid
import logging
import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from speech_to_text import transcribe_audio
from detect_language import detect_language
from translator import translate_text
from text_to_speech import text_to_speech
from chatbot import generate_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static directory for serving audio files
app.mount("/static", StaticFiles(directory="static/audio"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResponseOutput(BaseModel):
    query: str | None = None
    response: str
    audio_url: str
    error: str | None = None
    version: str = "2025-05-22"

@app.post("/process", response_model=ResponseOutput)
async def process_input(
    target_language: str = Form(...),
    model_name: str = Form(...),
    text: str = Form(None),
    audio: UploadFile = File(None),
):
    start_time = time.time()
    logger.info(f"Received request: target_language={target_language}, model_name={model_name}, text={text}, audio={audio.filename if audio else None}")

    # Create directories
    os.makedirs("audio", exist_ok=True)
    os.makedirs("static/audio", exist_ok=True)

    # Clean up old audio files (older than 1 hour)
    import glob
    for old_file in glob.glob("static/audio/output_audio_*.mp3"):
        if os.path.getmtime(old_file) < time.time() - 3600:
            os.remove(old_file)
            logger.info(f"Cleaned up old audio: {old_file}")

    # Step 1: Get input query
    audio_path = None
    query = None
    try:
        if audio:
            audio_path = os.path.join("audio", f"input_audio_{uuid.uuid4()}.wav")
            with open(audio_path, "wb") as f:
                content = await audio.read()
                f.write(content)
            logger.info(f"Wrote audio file: {audio_path}, size: {len(content)} bytes")
            
            # Verify file exists and is non-empty
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Failed to write audio file: {audio_path}")
            if os.path.getsize(audio_path) == 0:
                raise ValueError(f"Audio file is empty: {audio_path}")

            logger.info(f"Transcribing audio from {audio_path}")
            query_start = time.time()
            query = transcribe_audio(audio_path)
            logger.info(f"Transcription took {time.time() - query_start:.2f}s")
        else:
            query = text

        if not query:
            raise ValueError("No valid input provided")

        logger.info(f"Query: {query}")

        # Step 2: Detect and translate to English if needed
        detect_start = time.time()
        detected_lang = detect_language(query)
        logger.info(f"Detected language: {detected_lang}, took {time.time() - detect_start:.2f}s")
        if detected_lang != "en":
            translate_start = time.time()
            query_translated = translate_text(query, detected_lang, "en")
            logger.info(f"Translated query to English: {query_translated}, took {time.time() - translate_start:.2f}s")
        else:
            query_translated = query

        # Step 3: Generate chatbot response
        chatbot_start = time.time()
        response = generate_response(query_translated, model_name)
        logger.info(f"Chatbot response: {response}, took {time.time() - chatbot_start:.2f}s")

        # Step 4: Translate back to target language if needed
        if target_language.lower() != "english":
            translate_back_start = time.time()
            response = translate_text(response, "en", target_language.lower())
            logger.info(f"Translated response to {target_language}: {response}, took {time.time() - translate_back_start:.2f}s")

        # Step 5: Text-to-speech to generate audio
        audio_output_filename = f"output_audio_{uuid.uuid4()}.mp3"
        audio_output_path = os.path.join("static/audio", audio_output_filename)
        logger.info(f"Generating audio at {audio_output_path}")
        tts_start = time.time()
        text_to_speech(response, audio_output_path, target_language)
        logger.info(f"TTS generation took {time.time() - tts_start:.2f}s")

        # Verify audio file exists
        if not os.path.exists(audio_output_path):
            raise RuntimeError("Audio file was not created")

        # Step 6: Generate audio URL
        audio_url = f"/static/{audio_output_filename}"
        logger.info(f"Audio URL: {audio_url}")

        logger.info(f"Total request time: {time.time() - start_time:.2f}s")
        return ResponseOutput(query=query, response=response, audio_url=audio_url)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        error_response = str(e) if str(e) else "Unknown error"
        # Generate audio for error message
        audio_output_filename = f"output_audio_{uuid.uuid4()}.mp3"
        audio_output_path = os.path.join("static/audio", audio_output_filename)
        logger.info(f"Generating error audio at {audio_output_path}")
        try:
            text_to_speech(error_response, audio_output_path, target_language)
            audio_url = f"/static/{audio_output_filename}"
        except Exception as tts_e:
            logger.error(f"Failed to generate error audio: {str(tts_e)}")
            audio_url = ""
        return ResponseOutput(query=query, response=error_response, audio_url=audio_url, error=str(e))

    finally:
        # Cleanup input audio file
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info(f"Cleaned up input audio: {audio_path}")
            except Exception as e:
                logger.error(f"Failed to clean up {audio_path}: {str(e)}")