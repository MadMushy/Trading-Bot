import unittest
from backtest import run_backtest
from benchmark import buy_and_hold
from datetime import date, timedelta

class TestBackTest(unittest.TestCase):
    def test_no_trades(self):
        closing_prices = [100] * 30
        opening_prices = [100] * 30

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices)

        self.assertEqual(cash, 10000)
        self.assertEqual(shares, 0)
        self.assertEqual(portfolio_value, 10000)
        self.assertEqual(trades, [])
        self.assertEqual(len(equity_curve), 10)
        self.assertTrue(all(value == 10000 for value in equity_curve))

    def test_buy_trade(self):
        closing_prices = [100] * 20 + [110, 110]
        opening_prices = [100] * 20 + [110, 105]

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices)

        print(f"\nTrades: {trades}")
        print(f"Cash: {cash}")
        print(f"Shares: {shares}")
        print(f"Portfolio: {portfolio_value}")

        self.assertEqual(cash, 25)
        self.assertEqual(shares, 95)
        self.assertEqual(portfolio_value, 10475)
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["price"], 105)
        self.assertEqual(trades[0]["day"], 22)
        self.assertEqual(len(equity_curve), 2)

    def test_sell_trade(self):
        closing_prices = [100] * 20 + [110, 90, 90, 90]
        opening_prices = [100] * 20 + [110, 90, 90, 90]
    
        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices)

        print(f"\nTrades: {trades}")
        print(f"Cash: {cash}")
        print(f"Shares: {shares}")
        print(f"Portfolio: {portfolio_value}")

        self.assertEqual(cash, 10000)
        self.assertEqual(shares, 0)
        self.assertEqual(portfolio_value, 10000)
        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0]["action"], "BUY")
        self.assertEqual(trades[1]["action"], "SELL")
        self.assertEqual(len(equity_curve), 4)

    def test_length_strat_and_old(self):

        closing_prices = [100] * 30
        opening_prices = [100] * 30

        cash_strat, shares_strat, portfolio_value_strat, trades_strat, equity_curve = run_backtest(closing_prices, opening_prices)
        
        portfolio_value_buy, percent_return, equity_curve_buy = buy_and_hold(opening_prices, closing_prices, initial_cash=10000)

        self.assertEqual(len(equity_curve), 10)
        self.assertEqual(len(equity_curve_buy), 10)

    def test_next_day_execution(self):

        closing_prices = [100] * 20 + [110, 120]
        opening_prices = [100] * 20 + [110, 105]

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["action"], "BUY")
        self.assertAlmostEqual(trades[0]["price"], 105)
        self.assertEqual(shares, 95)
        self.assertAlmostEqual(portfolio_value, 11425)

    def test_backtest_with_slippage(self):

        closing_prices = [100] * 20 + [110, 120]
        opening_prices = [100] * 20 + [110, 105]

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices, slippage=.01)

        self.assertAlmostEqual(trades[0]["price"], 106.05)
        self.assertEqual(shares, 94)
        self.assertAlmostEqual(cash, 31.30)
        self.assertAlmostEqual(portfolio_value, 11311.30)

    def test_backtest_transaction_fee(self):

        closing_prices = [100] * 20 + [110, 120]
        opening_prices = [100] * 20 + [110, 105]

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices, transaction_fee=5.0)

        self.assertAlmostEqual(trades[0]["price"], 105.00)
        self.assertEqual(shares, 95)
        self.assertAlmostEqual(cash, 20.00)
        self.assertAlmostEqual(portfolio_value, 11420.00)

    def test_backtest_transaction_fee_2(self):

        closing_prices = [100] * 20 + [110, 90, 90, 90]
        opening_prices = [100] * 20 + [110, 90, 90, 90]

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices, transaction_fee=5.0)

        self.assertEqual(trades[0]["shares"], 111)
        self.assertAlmostEqual(trades[0]["price"], 90)
        self.assertAlmostEqual(trades[0]["cash"], 5)
        self.assertAlmostEqual(trades[1]["price"], 90)
        self.assertAlmostEqual(trades[1]["cash"], 9990)
        self.assertAlmostEqual(portfolio_value, 9990)

    def test_backtest_transaction_fee_valueerror(self):

        opening_prices = [100] * 20 + [50, 60]
        closing_prices = [100] * 20 + [50, 60]

        with self.assertRaises(ValueError):
            run_backtest(closing_prices, opening_prices, transaction_fee=-5.0)

    def test_buy_and_hold_slippage_transaction_fee(self):

        closing_prices = [100] * 20 + [110, 120]
        opening_prices = [100] * 20 + [110, 105]

        portfolio_value_final, percent_return, equity_curve = buy_and_hold(opening_prices, closing_prices, slippage=.01, transaction_fee=5.0)

        self.assertAlmostEqual(portfolio_value_final, 11306.30)
        self.assertAlmostEqual(percent_return, 13.063)

    def test_backtest_with_trades_matching(self):

        closing_prices = [100] * 20 + [110, 120]
        opening_prices = [100] * 20 + [110, 105]
        trades = [100] * 22

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices, slippage=0.01, dates=trades)

        self.assertAlmostEqual(trades[0]["price"], 106.05)
        self.assertEqual(shares, 94)
        self.assertAlmostEqual(cash, 31.30)
        self.assertAlmostEqual(portfolio_value, 11311.30)

    def test_backtest_with_trades_valueerror(self):

        closing_prices = [100] * 20 + [110, 120]
        opening_prices = [100] * 20 + [110, 105]
        trades = [100] * 21

        with self.assertRaises(ValueError):
            run_backtest(closing_prices, opening_prices, slippage=0.01, dates=trades)

    def test_backtest_with_dividends(self):

        closing_prices = [100] * 20 + [110] * 15
        opening_prices = closing_prices.copy()
        start_date = date(2026, 10, 1)
        dates = [
        (start_date + timedelta(days=i)).isoformat()
        for i in range(len(closing_prices))
        ]
        dividend_event = [
            {
                "ex_date": dates[23],
                "payment_date": dates[27],
                "amount_per_share": 1.50
            }
        ]
        result = run_backtest(
            closing_prices,
            opening_prices,
            initial_cash=10000,
            dates=dates,
            dividend_events=dividend_event

        )
        
        self.assertAlmostEqual(result[0], 235)

    def test_backtest_with_dividends_buy_on_ex_date(self):

        closing_prices = [100] * 20 + [110] * 15
        opening_prices = closing_prices.copy()
        start_date = date(2026, 10, 1)
        dates = [
        (start_date + timedelta(days=i)).isoformat()
        for i in range(len(closing_prices))
        ]
        dividend_event = [
            {
                "ex_date": dates[21],
                "payment_date": dates[25],
                "amount_per_share": 1.50
            }
        ]
        result = run_backtest(
            closing_prices,
            opening_prices,
            initial_cash=10000,
            dates=dates,
            dividend_events=dividend_event

        )
        
        self.assertAlmostEqual(result[0], 100)

    def test_backtest_with_dividends_sell_on_ex_date(self):

        closing_prices = [100] * 20 + [110] * 10 + [90] * 10
        opening_prices = closing_prices.copy()
        start_date = date(2026, 10, 1)
        dates = [
        (start_date + timedelta(days=i)).isoformat()
        for i in range(len(closing_prices))
        ]
        dividend_event = [
            {
                "ex_date": dates[32],
                "payment_date": dates[35],
                "amount_per_share": 1.50
            }
        ]
        result = run_backtest(
            closing_prices,
            opening_prices,
            initial_cash=10000,
            dates=dates,
            dividend_events=dividend_event

        )
        
        self.assertAlmostEqual(result[0], 8335.0)
        self.assertEqual(result[1], 0)
