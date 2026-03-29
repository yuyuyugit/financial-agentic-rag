from dataclasses import dataclass

@dataclass
class FinancialDocument:
    title: str
    content: str
    doc_type: str
    ticker: str
    date: str
