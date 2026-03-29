import os
import weaviate
from fastapi import FastAPI
from pydantic import BaseModel
from src.router import IntentRouter
from src.agent.graph import run_agent
from src.retrieval.keyword_search import KeywordSearcher

app = FastAPI(title="Financial Agentic RAG API")

router = IntentRouter()
searcher = KeywordSearcher()


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
    try:
        query_type = router.route(req.query)

        if query_type == "SIMPLE":
            result = searcher.search(req.query)
            return {"answer": result["result"], "query_type": "simple", "source": "keyword_search"}
        elif query_type == "COMPLEX":
            answer = run_agent(req.query)
            return {"answer": answer, "query_type": "complex", "source": "agent"}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "query_type": "error"}
