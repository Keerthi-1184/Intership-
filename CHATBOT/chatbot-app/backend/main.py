from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    model: str
    messages: list
    temperature: float = 0.7
    max_tokens: int = 1024
    image_url: str = None

@app.post("/chat")
async def chat_completion(request: ChatRequest):
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
    "model": request.model,
    "messages": request.messages,
    "temperature": request.temperature,
    "stream": False
}

    
    try:
        # Forward to Ollama's API
        ollama_url = "http://localhost:11434/api/chat"
        response = requests.post(ollama_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)