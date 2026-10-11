from market_data import get_closing_prices, get_data
from strategy import calculate_sma, generate_signal


def main():

	prices = get_closing_prices()

	sma = calculate_sma(prices, 5)
	print(f"5-day SMA: ${sma:.2f}")

	signal = generate_signal(prices)
	print(f"Signal For Bot: {signal}")

	data = get_data()
	print(data.get("current_user_url"))

if __name__ == "__main__":
	main()
