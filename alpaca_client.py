import os
from decimal import Decimal
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient


#load the credentials
load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

#Initialize the Trading Client
trading_client = TradingClient(
    api_key,
    secret_key,
    paper=True
)

def get_account_info():
    
    account = trading_client.get_account()
    cash = Decimal(account.cash)
    status= account.status
    portfolio_value = Decimal(account.portfolio_value)

    return status, cash, portfolio_value

def get_all_positions():

    positions = trading_client.get_all_positions()

    return positions
