# from gtts import gTTS
# import os

# # Language mapping
# LANGUAGE_CODES = {
#     "english": "en",
#     "hindi": "hi",
#     "spanish": "es",
#     "french": "fr",
#     "german": "de"
# }

# def text_to_speech(text: str, output_path: str, lang_name: str = "english"):
#     lang_code = LANGUAGE_CODES.get(lang_name.lower())

#     if not lang_code:
#         raise ValueError(f"Language not supported: {lang_name}")

#     try:
#         tts = gTTS(text=text, lang=lang_code)
#         tts.save(output_path)
#     except Exception as e:
#         raise RuntimeError(f"TTS generation failed: {str(e)}")

from gtts import gTTS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LANGUAGE_CODES = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "hindi": "hi",
}

def text_to_speech(text: str, output_path: str, lang_name: str = "english"):
    lang_code = LANGUAGE_CODES.get(lang_name.lower())
    if not lang_code:
        logger.error(f"Language not supported: {lang_name}")
        raise ValueError(f"Language not supported: {lang_name}")
    try:
        logger.info(f"Generating TTS for text: {text}, lang: {lang_code}, output: {output_path}")
        tts = gTTS(text=text, lang=lang_code)
        tts.save(output_path)
        logger.info(f"Audio saved at: {output_path}")
    except Exception as e:
        logger.error(f"TTS generation failed: {str(e)}")
        raise RuntimeError(f"TTS generation failed: {str(e)}")