from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils import query_ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    model: str = "deepseek-r1:1.5b"

@app.post("/chat")
def chat(req: ChatRequest):
    response = query_ollama(req.model, req.prompt)
    return {"response": response}
