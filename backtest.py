from strategy import generate_signal
from corporate_actions import record_dividend_entitlement, process_dividend_payments

def run_backtest(
        closing_prices, 
        opening_prices, 
        initial_cash=10000, 
        verbose=False,
        slippage=0.0,
        transaction_fee=0.0,
        dates=None,
        dividend_events=None

    ):
    cash = initial_cash
    shares = 0
    trades = []
    equity_curve = [initial_cash]
    pending_dividends = []

    if len(closing_prices) < 21:
        raise ValueError("At least 21 closing prices required")

    if len(closing_prices) != len(opening_prices):
        raise ValueError("Opening and closing prices must have same length.")
    
    if transaction_fee < 0:
        raise ValueError("Transaction fee cannot be negative")

    if dates is not None:
        if len(closing_prices) != len(dates):
            raise ValueError("Closing prices and dates must match")


	#Will only loop after at least 21 pieces of data
    for i in range(20, len(closing_prices) - 1):
        historical_prices = closing_prices[:i + 1]
        signal = generate_signal(historical_prices)
        if verbose:
            print(
                f"Signal Date: {dates[i]} |"
                f"Execution date: {dates[i + 1]} |"
                f"Current Price: ${closing_prices[i]:.2f} |"
                f"Signal: {signal}"
            )

        #Dividend entitlement check
        if dates is not None:
            current_date = dates[i + 1]
            
            #Entitlement recording
            if dividend_events is not None:
                for event in dividend_events:
                    if current_date == event["ex_date"] and shares > 0:
                        pending_dividends = record_dividend_entitlement(
                                pending_dividends,
                                shares,
                                event["amount_per_share"],
                                event["payment_date"]
                        )
            #If there are bending dividends pay them
            cash, pending_dividends = process_dividend_payments(
                pending_dividends,
                current_date,
                cash
            )

        #Log data when buy signal happens and execute trade
        execution_price = opening_prices[i + 1]
        if signal == "BUY":
            avalible_cash = cash - transaction_fee
            adjusted_execution_price = execution_price + (execution_price * slippage)
            if shares == 0:
                shares_to_buy = int(avalible_cash // adjusted_execution_price)
                if shares_to_buy > 0:
                    cash -= (shares_to_buy * adjusted_execution_price) + transaction_fee
                    shares += shares_to_buy
                    trade = {
                        "day": i + 2,
                        "date": dates[i + 1] if dates is not None else None,
                        "action": signal,
                        "price": adjusted_execution_price,
                        "shares": shares_to_buy,
                        "cash": cash
                    }

                    trades.append(trade)
        #Log data when sell signal happens and execute trade
        elif signal == "SELL":
            avalible_cash = cash - transaction_fee
            adjusted_execution_price = execution_price - (execution_price * slippage)
            if shares > 0:
                cash_to_add = shares * adjusted_execution_price - transaction_fee
                cash += cash_to_add
                trade = {
                    "day": i + 2,
                    "date": dates[i + 1] if dates is not None else None,
                    "action": signal,
                    "price": adjusted_execution_price,
                    "shares": shares,
                    "cash": cash
                }
                trades.append(trade)
                shares = 0

        #Gather information for equity curve
        daily_portfolio_value = cash + shares * closing_prices[i + 1]
        equity_curve.append(daily_portfolio_value)

    last_price = closing_prices[-1]
    portfolio_value = cash + shares * last_price 

    return cash, shares, portfolio_value, trades, equity_curve
