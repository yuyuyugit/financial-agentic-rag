import os
import weaviate
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Financial Agentic RAG API")


@app.get("/")
def root():
    return {"message": "Financial Agentic RAG Demo", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/test-weaviate")
def test_weaviate():
    url = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
    try:
        client = weaviate.Client(url)
        client.schema.get()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": "not implemented", "query_type": "unknown"}
