from decimal import Decimal
from strategy import update_strategy_state
from position_sizing import calculate_target_shares

def calculate_strategy_target(
    signal,
    previous_state,
    capital,
    allocation,
    share_price
):
    #Calculate current state
    state = update_strategy_state(signal, previous_state)

    #Get target quantity based on new state
    if state == "OUT":
        target_qty = 0
    if state == "INVESTED":
        target_qty = calculate_target_shares(capital, allocation, share_price)

    #Create a dictionary of the results
    target_dict = {
        "state" : state,
        "target_qty": target_qty
    }

    return target_dict
