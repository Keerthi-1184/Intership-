# backend/utils.py

def clean_text(text):
    return text.strip() if text else ""

def format_for_llm(text):
    # Ensure the text is clean and formatted for LLM input
    return clean_text(text) if text else "No content available."