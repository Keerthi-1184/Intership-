from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.graph_rag import GraphRAG

app = FastAPI(title="GraphRAG Chatbot")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    try:
        rag = GraphRAG()
        response = rag.query(request.query)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)