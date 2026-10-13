from strategy import generate_signal


def run_backtest(prices, initial_cash=10000):
	cash = initial_cash
	shares = 0

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

		if signal == "BUY":
			if shares == 0:
				shares_to_buy = int(cash // prices[i])
				cash -= shares_to_buy * prices[i]
				shares += shares_to_buy
		elif signal == "SELL":
			if shares > 0:
				cash_to_add = shares * prices[i]
				cash += cash_to_add
				shares = 0

	last_price = prices[-1]
	portfolio_value = cash + shares * last_price 

	return cash, shares, portfolio_value
