import os
import yaml
import weaviate
import weaviate.classes as wvc
from openai import OpenAI
from pathlib import Path

_client = None
_embedder = None
_embed_cfg = None

def _load_embed_cfg():
    global _embed_cfg
    if _embed_cfg is None:
        cfg_path = Path(__file__).parents[2] / "config" / "embedding.yaml"
        with open(cfg_path) as f:
            _embed_cfg = yaml.safe_load(f)
    return _embed_cfg

def get_client() -> weaviate.WeaviateClient:
    global _client
    if _client is None:
        url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        host, port = url.rsplit(":", 1) if ":" in url.split("//")[-1] else (url, "8080")
        host = host.replace("http://", "").replace("https://", "")
        _client = weaviate.connect_to_custom(
            http_host=host,
            http_port=int(port),
            http_secure=False,
            grpc_host=host,
            grpc_port=50051,
            grpc_secure=False,
        )
    return _client

def get_embedding(text: str) -> list[float]:
    global _embedder
    if _embedder is None:
        cfg = _load_embed_cfg()
        _embedder = OpenAI(
            api_key=os.getenv(cfg["api_key_env"]),
            base_url=cfg["base_url"]
        )
    return _embedder.embeddings.create(model=_load_embed_cfg()["model"], input=text).data[0].embedding

def schema_exists(client: weaviate.WeaviateClient) -> bool:
    return client.collections.exists("FinancialDocument")

def create_schema(client: weaviate.WeaviateClient):
    if schema_exists(client):
        return
    client.collections.create(
        name="FinancialDocument",
        vectorizer_config=wvc.config.Configure.Vectorizer.none(),
        properties=[
            wvc.config.Property(name=name, data_type=wvc.config.DataType.TEXT)
            for name in ["title", "content", "doc_type", "ticker", "date"]
        ]
    )
