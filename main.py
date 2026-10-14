from market_data import get_closing_prices, get_data
from strategy import calculate_sma, generate_signal
from backtest import run_backtest
from performance import calculate_return

def main():

    prices = get_closing_prices()

    sma = calculate_sma(prices, 5)
    print(f"5-day SMA: ${sma:.2f}")

    l_sma = calculate_sma(prices, 20)
    print(f"20-day SMA: ${l_sma:.2f}")

    signal = generate_signal(prices)
    print(f"Signal For Bot: {signal}")

    data = get_data()
    print(data.get("current_user_url"))

    cash, shares, portfolio_value, trades, equity_curve = run_backtest(prices)

    total_return = calculate_return(10000, portfolio_value)

    print(f"Total Return: {total_return:.2f}%",
          f"Trades Executed: {len(trades)}")

if __name__ == "__main__":
	main()
