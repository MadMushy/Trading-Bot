from decimal import Decimal
from strategy import update_strategy_state
from position_sizing import calculate_target_shares

def calculate_strategy_target(
    signal,
    previous_state,
    previous_target_qty,
    capital,
    allocation,
    share_price
):
    if type(previous_target_qty) is not int or previous_target_qty < 0:
        raise ValueError("Previous target quantity cannot be negative or not an integer.")
    if previous_state == "OUT" and previous_target_qty != 0:
        raise ValueError("Invalid previous state and previous target quantity")
    
    #Calculate current state
    state = update_strategy_state(signal, previous_state)

    #Get target quantity based on new state
    if signal == "BUY":
        target_qty = calculate_target_shares(capital, allocation, share_price)
    elif signal == "SELL":
        target_qty = 0
    else:
        target_qty = previous_target_qty

    #Create a dictionary of the results
    target_dict = {
        "state" : state,
        "target_qty": target_qty
    }

    return target_dict
