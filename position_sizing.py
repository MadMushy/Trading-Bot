from decimal import Decimal, InvalidOperation

def calculate_target_shares(capital, allocation, share_price):
    
    try:
        capital = Decimal(str(capital))
        allocation = Decimal(str(allocation))
        share_price = Decimal(str(share_price))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("invalid value") from exc

    if not capital.is_finite() or capital < 0:
        raise ValueError("Capital needs to be finite and nonnegative")
    if not allocation.is_finite() or not 0 <= allocation <= 1:
        raise ValueError("Allocation needs to be finite and between 0 and 1")
    if not share_price.is_finite() or share_price <= 0:
        raise ValueError("Share price needs to be finite and greater than 0")

    budget = capital * allocation
    shares = int(budget // share_price)

    return shares
