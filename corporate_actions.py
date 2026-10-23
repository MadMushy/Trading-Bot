def calculate_dividend_payment(shares, dividend_per_share):

    if shares < 0:
        raise ValueError("Share price cannot be negative")
    if dividend_per_share < 0:
        raise ValueError("Dividend cannot be negative")

    payment = shares * dividend_per_share

    return payment

def record_dividend_entitlement(
        pending_dividends,
        shares,
        dividend_per_share,
        payment_date
    ):

    #Calculate payment
    payment = calculate_dividend_payment(shares, dividend_per_share)

    #Record payment
    record = {
            "payment_date": payment_date,
            "amount": payment
            }

    if payment != 0:
        pending_dividends.append(record)

    return pending_dividends
