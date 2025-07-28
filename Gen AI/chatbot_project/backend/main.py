from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from model_handler import query_model
 
app = FastAPI()
 
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
class ChatRequest(BaseModel):
    model_name: str
    messages: list  # Includes full history: [{"role": "user", "content": "..."}, ...]
 
@app.post("/chat/")
def chat_endpoint(req: ChatRequest):
    reply = query_model(req.model_name, req.messages)
    return {"response": reply}
 
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 