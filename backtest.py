from strategy import generate_signal

def run_backtest(closing_prices, opening_prices, initial_cash=10000, verbose=False):
    cash = initial_cash
    shares = 0
    trades = []
    equity_curve = []

    if len(closing_prices) < 21:
        raise ValueError("At least 21 closing prices required")

    if len(closing_prices) != len(opening_prices):
        raise ValueError("Opening and closing prices must have same length.")

	#Will only loop after at least 21 pieces of data
    for i in range(20, len(closing_prices) - 1):
        historical_prices = closing_prices[:i + 1]
        signal = generate_signal(historical_prices)
        if verbose:
            print(
                f"Day {i + 1} |"
                f"Current Price: ${closing_prices[i]:.2f} |"
                f"Signal: {signal}"

            )
        #Log data when buy signal happens and execute trade
        execution_price = opening_prices[i + 1]
        if signal == "BUY":
            if shares == 0:
                shares_to_buy = int(cash // execution_price)
                if shares_to_buy > 0:
                    cash -= shares_to_buy * execution_price
                    shares += shares_to_buy
                    trade = {
                        "day": i + 2,
                        "action": signal,
                        "price": execution_price,
                        "shares": shares_to_buy
                    }

                    trades.append(trade)
        #Log data when sell signal happens and execute trade
        elif signal == "SELL":
            if shares > 0:
                cash_to_add = shares * execution_price
                cash += cash_to_add
                trade = {
                    "day": i + 2,
                    "action": signal,
                    "price": execution_price,
                    "shares": shares
                }
                trades.append(trade)
                shares = 0

        #Gather information for equity curve
        daily_portfolio_value = cash + shares * closing_prices[i + 1]
        equity_curve.append(daily_portfolio_value)

    last_price = closing_prices[-1]
    portfolio_value = cash + shares * last_price 

    return cash, shares, portfolio_value, trades, equity_curve
