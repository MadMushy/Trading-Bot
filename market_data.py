import os
import requests
from dotenv import load_dotenv
from alpaca.data.enums import Adjustment
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
        start=datetime(2022, 9, 1, tzinfo=timezone.utc),
        end=datetime(2026, 10, 27, tzinfo=timezone.utc),
        feed="iex",
        adjustment=Adjustment.RAW
    )
    bars = client.get_stock_bars(request)

    # Collect all closing prices and opening prices and trading dates
    closing_prices = []
    opening_prices = []
    trading_dates = []

    for bar in bars["SPY"]:
        closing_prices.append(bar.close)
        opening_prices.append(bar.open)
        trading_dates.append(bar.timestamp.date().isoformat())

    return closing_prices, opening_prices, trading_dates

def get_data():
    url = "https://api.github.com"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed: {response.status_code}")
        return None

