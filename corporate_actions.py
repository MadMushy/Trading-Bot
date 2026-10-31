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

    if dividend_per_share < 0:
        raise ValueError("Dividend can not be negative")

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

def process_dividend_payments(pending_dividends, current_date, cash):
    updated_pending_dividends = []

    if cash < 0:
        raise ValueError("Cash balance cannot be negative")

    for dividend in pending_dividends:
        if dividend["amount"] < 0:
            raise ValueError("Dividend cannot be negative")

        if dividend["payment_date"] <= current_date:
            cash += dividend["amount"]
        else:
            updated_pending_dividends.append(dividend)

    return cash, updated_pending_dividends

def apply_stock_split(shares, split_ratio):

    if split_ratio <= 0:
        raise ValueError("Split ration cannot be less than or equal to zero")

    new_shares = shares * split_ratio

    return new_shares

def adjust_prices_for_splits(prices, dates, split_events):
    adj_prices = prices.copy()

    for i in range(len(dates)):
        for event in split_events:
            #Acessing a list so index like so
            if dates[i] < event["ex_date"]:
                #Updste adjusted prices based on index
                adj_prices[i] = adj_prices[i] / event["split_ratio"]
            else:
                adj_prices[i] = adj_prices[i]

    return adj_prices
