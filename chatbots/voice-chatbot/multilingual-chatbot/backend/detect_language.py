from langdetect import detect

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "en"  # Default to English if detection fails