# import whisper

# def transcribe_audio(audio_path: str) -> str:
#     try:
#         model = whisper.load_model("base")
#         result = model.transcribe(audio_path)
#         return result["text"]
#     except Exception as e:
#         return f"Error in transcription: {str(e)}"


import whisper
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def transcribe_audio(audio_path: str) -> str:
    try:
        # Validate audio file
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        file_size = os.path.getsize(audio_path)
        if file_size == 0:
            logger.error(f"Audio file is empty: {audio_path}")
            raise ValueError(f"Audio file is empty: {audio_path}")
        
        logger.info(f"Transcribing audio file: {audio_path}, size: {file_size} bytes")

        # Load Whisper model
        model = whisper.load_model("tiny")  # Smallest model for speed
        logger.info("Whisper model loaded")

        # Transcribe audio
        result = model.transcribe(audio_path, fp16=False)
        transcription = result["text"].strip()
        
        if not transcription:
            logger.warning(f"Transcription empty for {audio_path}")
            raise ValueError("Transcription resulted in empty text")
        
        logger.info(f"Transcription: {transcription}")
        return transcription

    except Exception as e:
        logger.error(f"Error in transcription: {str(e)}")
        raise