import os
import uuid
from decimal import Decimal
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderStatus

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

def create_market_order(symbol, quantity, client_order_id=None):
    
    if quantity <= 0:
        raise ValueError("Quantity cannot be negative")
    if not isinstance(symbol, str):
        raise TypeError("Symbol needs to be a string")

    #Create a uniqe ID seperate from the Alpaca ID if there is no client order id
    if client_order_id is None:
        order_id = str(uuid.uuid4())
    else:
        order_id = client_order_id

    #Create an order
    market_order_data = MarketOrderRequest(
                        symbol=symbol,
                        qty=quantity,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY,
                        client_order_id=order_id
                        )

    return market_order_data

def submit_order(order_request):

    market_order = trading_client.submit_order(
                 order_data=order_request
                )
    return market_order

def is_valid_uuid(uuid_string):
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string.lower()
    except ValueError:
        return False

def get_order_by_id(order_id):

    if is_valid_uuid(order_id):
        #Verifies valid order id and then looks
        num = trading_client.get_order_by_id(order_id)
        return num
    else:
        raise ValueError("Not a valid order ID")

def get_order_by_client_id(client_order_id):

    if is_valid_uuid(client_order_id):
        #Verifies valid uuid
        num = trading_client.get_order_by_client_id(client_order_id)
        return num
    else:
        raise ValueError("Not a valid client ID")

def is_order_filled(order):

    if order is None:
        raise ValueError("Order cannot be None")
    if order.status is None:
        raise ValueError("Order status cannot be None.")

    if order.status == OrderStatus.FILLED:
        return True
    return False

def get_remaining_quantity(order):

    if order is None:
        raise ValueError("order cannot be None")

    order = Decimal(order.qty)
    filled = Decimal(order.filled_qty)

    if filled > order:
        raise ValueError("filled cannot be greater then order.")

    remaining_qty = order - filled
    
    return remaining_qty
