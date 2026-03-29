from langchain_core.tools import tool

PORTFOLIO = {
    "TSLA": {"shares": 50, "avg_price": 245.30},
    "NVDA": {"shares": 30, "avg_price": 875.20},
    "AAPL": {"shares": 100, "avg_price": 189.50},
}


@tool
def get_portfolio() -> str:
    """Get the current mock portfolio holdings and total value."""
    lines = []
    total = 0.0
    for ticker, data in PORTFOLIO.items():
        value = data["shares"] * data["avg_price"]
        total += value
        lines.append(f"{ticker}: {data['shares']} shares @ ${data['avg_price']:.2f} (${value:,.2f})")
    lines.append(f"Total value: ${total:,.2f}")
    return "\n".join(lines)
