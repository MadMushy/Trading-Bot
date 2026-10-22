def calculate_dividend_payment(shares, dividend_per_share):

    if shares < 0:
        raise ValueError("Share price cannot be negative")
    if dividend_per_share < 0:
        raise ValueError("Dividend cannot be negative")

    payment = shares * dividend_per_share

    return payment
