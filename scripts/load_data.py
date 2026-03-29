import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))

from src.retrieval.weaviate_client import get_client, create_schema, get_embedding

SAMPLE_DOCS = [
    {
        "title": "Tesla Q3 2024 Earnings Report",
        "content": "Tesla reported Q3 2024 revenue of $25.18B, up 8% YoY. Automotive revenue was $20.02B. Net income reached $2.17B. Vehicle deliveries totaled 462,890 units, a record quarter. Energy generation and storage revenue surged 52% to $2.38B.",
        "doc_type": "earnings_report",
        "ticker": "TSLA",
        "date": "2024-10-23",
    },
    {
        "title": "NVIDIA Q2 FY2025 Earnings Report",
        "content": "NVIDIA posted Q2 FY2025 revenue of $30.04B, up 122% YoY, driven by Data Center revenue of $26.3B. EPS of $0.68 beat estimates by $0.05. Gross margin expanded to 75.1%. Q3 guidance set at $32.5B, above consensus of $31.7B.",
        "doc_type": "earnings_report",
        "ticker": "NVDA",
        "date": "2024-08-28",
    },
    {
        "title": "Fed Rate Decision Sparks Tech Rally",
        "content": "The Federal Reserve held rates steady at 5.25-5.50% in its September meeting, signaling potential cuts in 2024. Technology stocks rallied broadly, with the Nasdaq gaining 1.8%. Growth stocks benefited most as long-duration assets repriced on lower rate expectations.",
        "doc_type": "financial_news",
        "ticker": "",
        "date": "2024-09-18",
    },
    {
        "title": "AI Chip Demand Drives Semiconductor Sector Outperformance",
        "content": "Semiconductor stocks outperformed the broader market in Q3 2024, led by AI infrastructure spending. Analysts cite hyperscaler capex commitments from Microsoft, Google, and Amazon as key demand drivers. Supply constraints for advanced packaging remain a bottleneck through 2025.",
        "doc_type": "financial_news",
        "ticker": "",
        "date": "2024-10-01",
    },
    {
        "title": "Tesla 12-Month Price Target Raised to $300",
        "content": "We raise our TSLA price target to $300 from $250, maintaining an Outperform rating. Our revised model reflects stronger-than-expected FSD adoption rates and improving energy storage margins. Key risks include EV price competition and execution on the Cybertruck ramp. We see 2025 deliveries reaching 2.1M units.",
        "doc_type": "analyst_report",
        "ticker": "TSLA",
        "date": "2024-11-05",
    },
]

if __name__ == "__main__":
    import weaviate.classes as wvc

    client = get_client()
    create_schema(client)

    collection = client.collections.get("FinancialDocument")
    objects = []
    for doc in SAMPLE_DOCS:
        vector = get_embedding(f"{doc['title']} {doc['content']}")
        objects.append(wvc.data.DataObject(properties=doc, vector=vector))

    collection.data.insert_many(objects)

    for i, doc in enumerate(SAMPLE_DOCS):
        print(f"[{i+1}/{len(SAMPLE_DOCS)}] Loaded: {doc['title']}")

    total = collection.aggregate.over_all(total_count=True).total_count
    print(f"\nDone. Total documents in Weaviate: {total}")

    client.close()
