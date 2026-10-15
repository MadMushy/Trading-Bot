import os
import requests
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timezone

# Load the credentials
load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
secret_key =os.getenv("ALPACA_SECRET_KEY")

# Initialize Historical Data Client
client = StockHistoricalDataClient(
    api_key,
    secret_key
)

def get_closing_prices():
    # Create a request for historical SPY
    request = StockBarsRequest(
        symbol_or_symbols="SPY",
        timeframe=TimeFrame.Day,
        start=datetime(2026, 9, 1, tzinfo=timezone.utc),
        end=datetime(2026, 10, 13, tzinfo=timezone.utc),
        feed="iex"
    )
    bars = client.get_stock_bars(request)

    # Collect all closing prices and opening prices
    closing_prices = []
    opening_prices = []

    for bar in bars["SPY"]:
        closing_prices.append(bar.close)
        opening_prices.append(bar.open)

    return closing_prices, opening_prices

def get_data():
    url = "https://api.github.com"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed: {response.status_code}")
        return None

