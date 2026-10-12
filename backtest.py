from strategy import generate_signal


def run_backtest(prices, initial_cash=10000):
	cash = initial_cash
	shares = 0

	for i in range(20, len(prices)):
		historical_prices = prices[:i + 1]
		signal = generate_signal(historical_prices)
		print(
			f"Day {i + 1} |"
			f"Current Price: ${prices[i]:.2f} |"
			f"Signal: {signal}"

		)

	return cash, shares
