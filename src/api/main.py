import os
import weaviate
from fastapi import FastAPI
from pydantic import BaseModel
from src.router import IntentRouter, QueryType
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
        client = weaviate.connect_to_custom(http_host=url.split("://")[1].split(":")[0],
                                            http_port=int(url.split(":")[-1]),
                                            http_secure=False,
                                            grpc_host=url.split("://")[1].split(":")[0],
                                            grpc_port=50051,
                                            grpc_secure=False)
        client.collections.list_all()
        client.close()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        query_type = router.route(req.query)

        if query_type == QueryType.SIMPLE:
            result = searcher.search(req.query)
            return {"answer": result["result"], "query_type": "simple", "source": "keyword_search"}
        elif query_type == QueryType.COMPLEX:
            answer = run_agent(req.query, intent="generate_answer")
            return {"answer": answer, "query_type": "complex", "source": "agent"}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "query_type": "error"}
