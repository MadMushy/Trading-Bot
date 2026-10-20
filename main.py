from market_data import get_closing_prices, get_data
from strategy import calculate_sma, generate_signal
from backtest import run_backtest
from performance import calculate_return, calculate_max_drawdown, calculate_sharpe_ratio, calculate_daily_returns
from benchmark import buy_and_hold

def main():

    closing_prices, opening_prices = get_closing_prices()

    sma = calculate_sma(closing_prices, 5)
    print(f"5-day SMA: ${sma:.2f}")

    l_sma = calculate_sma(closing_prices, 20)
    print(f"20-day SMA: ${l_sma:.2f}")

    signal = generate_signal(closing_prices)
    print(f"Signal For Bot: {signal}")

    data = get_data()
    print(data.get("current_user_url"))

    initial_cash = 10000
    #Cross over strat
    cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices)
    total_return = calculate_return(10000, portfolio_value)
    max_drawdown = calculate_max_drawdown(equity_curve)
    
    #Buy and hold strat
    portfolio_value_buy_and_hold, buy_and_hold_return, equity_curve_buy_and_hold = buy_and_hold(opening_prices, closing_prices, initial_cash)

    buy_and_hold_drawdown = calculate_max_drawdown(equity_curve_buy_and_hold)

    #Calculate daily returns for Sharpe Ratio
    daily_return_cross_over = calculate_daily_returns(equity_curve)
    daily_return_buy_and_hold = calculate_daily_returns(equity_curve_buy_and_hold)

    #Calculate Sharpe Ratio
    sharpe_ratio_cross_over = calculate_sharpe_ratio(daily_return_cross_over)
    sharpe_ratio_buy_and_hold = calculate_sharpe_ratio(daily_return_buy_and_hold)

    print("========== BACKTEST RESULTS ==========\n"
          f"Inital Capital:   ${initial_cash:,.2f}\n"
          f"Final Portfolio:  ${portfolio_value:,.2f}\n"
          f"Total Return:      {total_return:.2f}\n"
          f"Maximum Drawdown:  {max_drawdown:.2f}\n"
          f"Trades Executed:   {len(trades)}\n"
          f"Remaining Cash:   ${cash:,.2f}\n"
          f"Shares Held:       {shares}\n"
          f"Sharpe Ratio:      {sharpe_ratio_cross_over:.2f}\n\n"
          f"B&H Portfolio     ${portfolio_value_buy_and_hold:,.2f}\n"
          f"B&H Return %:      {buy_and_hold_return:.2f}\n"
          f"B&H Drawdown:      {buy_and_hold_drawdown:.2f}\n"
          f"Sharpe Ratio:      {sharpe_ratio_buy_and_hold:.2f}\n"
          f"======================================="
            
            )

    print(f"Total Return: {total_return:.2f}%",
          f"Trades Executed: {len(trades)}")

    print(len(closing_prices))
    print(len(opening_prices))

if __name__ == "__main__":
	main()
