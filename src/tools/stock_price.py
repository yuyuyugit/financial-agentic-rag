import yfinance as yf
from langchain_core.tools import tool


@tool
def get_stock_price(ticker: str) -> str:
    """Get the current stock price and daily change for a given ticker symbol."""
    try:
        hist = yf.Ticker(ticker).history(period="1d")
        if hist.empty:
            return f"No data found for {ticker}"
        price = hist["Close"].iloc[-1]
        change = (price - hist["Open"].iloc[-1]) / hist["Open"].iloc[-1] * 100
        return f"{ticker} current price: ${price:.2f}, change: {change:+.2f}%"
    except Exception as e:
        return f"Error fetching {ticker}: {e}"
