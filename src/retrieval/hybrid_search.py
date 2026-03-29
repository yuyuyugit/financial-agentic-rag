import weaviate
import weaviate.classes as wvc
from .weaviate_client import get_embedding

COLLECTION = "FinancialDocument"
PROPS = ["title", "content", "doc_type", "ticker"]

def _to_dict(obj, certainty=None) -> dict:
    p = obj.properties
    return {k: p.get(k) for k in PROPS} | {"certainty": certainty}

def vector_search(client: weaviate.WeaviateClient, query: str, limit: int = 5) -> list[dict]:
    col = client.collections.get(COLLECTION)
    vector = get_embedding(query)
    res = col.query.near_vector(near_vector=vector, limit=limit, return_metadata=wvc.query.MetadataQuery(certainty=True))
    return [_to_dict(o, o.metadata.certainty) for o in res.objects]

def bm25_search(client: weaviate.WeaviateClient, query: str, limit: int = 5) -> list[dict]:
    col = client.collections.get(COLLECTION)
    res = col.query.bm25(query=query, limit=limit)
    return [_to_dict(o) for o in res.objects]

def hybrid_search(client: weaviate.WeaviateClient, query: str, alpha: float = 0.5, limit: int = 5) -> list[dict]:
    col = client.collections.get(COLLECTION)
    vector = get_embedding(query)
    res = col.query.hybrid(query=query, vector=vector, alpha=alpha, limit=limit, return_metadata=wvc.query.MetadataQuery(score=True))
    seen, results = set(), []
    for o in res.objects:
        title = o.properties.get("title")
        if title not in seen:
            seen.add(title)
            results.append(_to_dict(o, o.metadata.score))
    return results
