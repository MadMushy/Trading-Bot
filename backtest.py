from strategy import generate_signal

def run_backtest(prices, initial_cash=10000):
    cash = initial_cash
    shares = 0
    trades = []
    equity_curve = []

    if len(prices) < 21:
        raise ValueError("At least 21 closing prices required")

	#Will only loop after at least 21 pieces of data
    for i in range(20, len(prices)):
        historical_prices = prices[:i + 1]
        signal = generate_signal(historical_prices)
        print(
            f"Day {i + 1} |"
            f"Current Price: ${prices[i]:.2f} |"
            f"Signal: {signal}"

        )
        #Log data when buy signal happens
        if signal == "BUY":
            if shares == 0:
                shares_to_buy = int(cash // prices[i])
                cash -= shares_to_buy * prices[i]
                shares += shares_to_buy
                if shares_to_buy > 0:
                    trade = {
                        "day": i + 1,
                        "action": signal,
                        "price": prices[i],
                        "shares": shares_to_buy
                    }

                    trades.append(trade)
        #Log data when sell signal happens
        elif signal == "SELL":
            if shares > 0:
                cash_to_add = shares * prices[i]
                cash += cash_to_add
                trade = {
                    "day": i + 1,
                    "action": signal,
                    "price": prices[i],
                    "shares": shares_to_buy
                }
                trades.append(trade)
                shares = 0

        #Gather information for equity curve
        daily_portfolio_value = cash + shares * prices[i]
        equity_curve.append(daily_portfolio_value)

    last_price = prices[-1]
    portfolio_value = cash + shares * last_price 

    return cash, shares, portfolio_value, trades, equity_curve
