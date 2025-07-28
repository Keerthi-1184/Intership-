import requests
 
API_URL = "http://localhost:11434/v1/chat/completions"
 
def query_model(model_name: str, messages: list):
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
 
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"
 