from performance import calculate_return

def buy_and_hold(opening_prices, closing_prices, initial_cash=10000):

    if len(opening_prices) != len(closing_prices):
        raise ValueError("Opening and closing prices must match")

    if len(opening_prices) < 21:
        raise ValueError("Need at least 21 points of data")

    cash = initial_cash
    execution_price = opening_prices[21]
    shares = 0
    equity_curve =[initial_cash]
    
    #Buy shares
    shares_to_buy = int(initial_cash // execution_price)
    cash -= shares_to_buy * execution_price
    shares += shares_to_buy

    last_price = closing_prices[-1]

    portfolio_value_final = cash + (shares * last_price)
    portfolio_value_initial = cash + (shares * execution_price)

    #Gather information for equity curve
    for i in range(21, len(closing_prices)):
        daily_value = cash + shares * closing_prices[i]
        equity_curve.append(daily_value)

    
    #Calculate % return
    percent_return = float(calculate_return(portfolio_value_initial, portfolio_value_final))

    return portfolio_value_final, percent_return, equity_curve
