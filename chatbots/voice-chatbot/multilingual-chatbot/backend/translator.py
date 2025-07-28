from googletrans import Translator

def translate_text(text: str, src_lang: str, dest_lang: str) -> str:
    try:
        translator = Translator()
        # Map to googletrans language codes
        lang_map = {
            "english": "en",
            "spanish": "es",
            "french": "fr",
            "german": "de",
            "hindi": "hi"
        }
        dest_lang_code = lang_map.get(dest_lang.lower(), "en")
        result = translator.translate(text, src=src_lang, dest=dest_lang_code)
        return result.text
    except Exception as e:
        return f"Error in translation: {str(e)}"