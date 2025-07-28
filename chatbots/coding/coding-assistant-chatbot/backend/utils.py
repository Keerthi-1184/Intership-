import requests

def query_ollama(model: str, prompt: str, images: list = None):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    if images:
        payload["images"] = images

    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return response.json().get("response", "No response from model.")
