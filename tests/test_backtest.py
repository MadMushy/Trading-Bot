import unittest
from backtest import run_backtest

class TestBackTest(unittest.TestCase):
    def test_no_trades(self):
        prices = [100] * 30

        cash, shares, portfolio_value, trades = run_backtest(prices)

        self.assertEqual(cash, 10000)
        self.assertEqual(shares, 0)
        self.assertEqual(portfolio_value, 10000)
        self.assertEqual(trades, [])

    def test_buy_trade(self):
        prices = [100] * 20 + [110]

        cash, shares, portfolio_value, trades = run_backtest(prices)

        self.assertEqual(cash, 100)
        self.assertEqual(shares, 90)
        self.assertEqual(portfolio_value, 10000)
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["action"], "BUY")

    def test_sell_trade(self):
        prices = [100] * 20 + [110, 90, 90]
    
        cash, shares, portfolio_value, trades = run_backtest(prices)

        self.assertEqual(cash, 8200)
        self.assertEqual(shares, 0)
        self.assertEqual(portfolio_value, 8200)
        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0]["action"], "BUY")
        self.assertEqual(trades[1]["action"], "SELL")
