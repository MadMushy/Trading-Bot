from market_data import closing_prices
from strategy import calculate_sma

def main():
	sma = calculate_sma(closing_prices, 5)
	print(f"5-day SMA: ${sma:.2f}")

if __name__ == "__main__":
	main()
