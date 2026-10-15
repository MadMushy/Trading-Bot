import unittest
from backtest import run_backtest

class TestBackTest(unittest.TestCase):
    def test_no_trades(self):
        closing_prices = [100] * 30
        opening_prices = [100] * 30

        cash, shares, portfolio_value, trades, equity_curve = run_backtest(closing_prices, opening_prices)

        self.assertEqual(cash, 10000)
        self.assertEqual(shares, 0)
        self.assertEqual(portfolio_value, 10000)
        self.assertEqual(trades, [])
        self.assertEqual(len(equity_curve), 9)
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
        self.assertEqual(len(equity_curve), 1)

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
        self.assertEqual(len(equity_curve), 3)
