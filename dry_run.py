from alpaca_client import evaluate_position
from decimal import Decimal, InvalidOperation


def main():
    symbol = "SPY"
    target_qty = Decimal("0")

    result = evaluate_position(symbol, target_qty)

    print(
            f"Symbol:           {result["symbol"]}\n"
            f"Target Quantity:  {result["target_qty"]}\n"
            f"Current Quantity: {result["current_qty"]}\n"
            f"Action:           {result["action"]}\n"
            f"Action Quantity:  {result["action_qty"]}"
    )

if __name__ == "__main__":
    main()
