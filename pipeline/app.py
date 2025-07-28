# Save as main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.post("/echo")
def echo_message(data: dict):
    return {"you_sent": data}
