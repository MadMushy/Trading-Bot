from decimal import Decimal
from portfolio import calculate_strategy_target
from alpaca_client import evaluate_position

def evaluate_strategy(
    symbol,
    signal,
    previous_state,
    previous_target_qty,
    capital,
    allocation,
    share_price
):
    #evaluate target dictionary for new state and target_qty
    target_dict = calculate_strategy_target(
            signal,
            previous_state,
            previous_target_qty,
            capital,
            allocation,
            share_price
    )

    #Asign them varibles
    new_state = target_dict["state"]
    target_qty = target_dict["target_qty"]

    #call evaluate position for current_qty, action, and action_qty
    action_dict = evaluate_position(symbol, target_qty)

    #Place all in a new dictionary
    new_dict = {
            "symbol": symbol,
            "signal": signal,
            "state": new_state,
            "target_qty": action_dict["target_qty"],
            "current_qty": action_dict["current_qty"],
            "action": action_dict["action"],
            "action_qty": action_dict["action_qty"]
    }

    return new_dict
