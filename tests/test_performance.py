import unittest
from performance import calculate_return, calculate_max_drawdown, calculate_daily_returns, calculate_sharpe_ratio
from benchmark import buy_and_hold


class TestPerformance(unittest.TestCase):

    def test_positive_return(self):

        result = calculate_return(10000, 12000)
        self.assertEqual(result, 20.0)

    def test_negative_return(self):

        result = calculate_return(10000, 8200)
        self.assertEqual(result, -18.0)

    def test_zero_return(self):

        result = calculate_return(10000, 10000)
        self.assertEqual(result, 0.0)

    def test_value_error(self):

        with self.assertRaises(ValueError):
            calculate_return(-10000, 12000)

    def test_equity_curve_30(self):

        equity_curve = [10000, 11000, 10500, 9000, 7700, 11500]
        result = calculate_max_drawdown(equity_curve)
        self.assertEqual(result, 30.0)

    def test_equity_curve_50(self):

        equity_curve = [10000, 12000, 6000, 9000]
        result = calculate_max_drawdown(equity_curve)
        self.assertEqual(result, 50.0)

    def test_equity_curve_zero_percent(self):

        equity_curve = [10000, 10500, 11000, 12000]
        result = calculate_max_drawdown(equity_curve)
        self.assertEqual(result, 0.0)

    def test_equity_curve_value_error(self):

        equity_curve = []

        with self.assertRaises(ValueError):
            calculate_max_drawdown(equity_curve)

    def test_buy_and_hold(self):
        closing_prices = [100] * 20 + [110, 110, 130]
        opening_prices = [100] * 20 + [110, 105, 125]

        portfolio_value_final, percent_return, equity_curve = buy_and_hold(opening_prices, closing_prices, initial_cash=10000)

        self.assertEqual(portfolio_value_final, 12375)
        self.assertEqual(percent_return, 23.75)

    def test_daily_returns(self):
        
        equity_curve = [10000, 10200, 10100]

        result = calculate_daily_returns(equity_curve)

        self.assertAlmostEqual(result[0], .02)
        self.assertAlmostEqual(result[1], -0.00980392156862745)

    def test_sharpe_ratio_1(self):

        daily_returns = [.01, -.01, .02, 0.0]

        sharpe_ratio = calculate_sharpe_ratio(daily_returns, risk_free_rate=0.0)

        self.assertAlmostEqual(sharpe_ratio, 6.148170459575759)

    def test_sharpe_ratio_2(self):

        daily_returns = [.01, -.01, .02, 0.0]

        sharpe_ratio = calculate_sharpe_ratio(daily_returns, risk_free_rate=.04)

        self.assertAlmostEqual(sharpe_ratio, 5.952990444986053)

    def test_sharpe_ratio_valueerror_1(self):

        daily_returns = [.01, .01, .01]

        with self.assertRaises(ValueError):
            calculate_sharpe_ratio(daily_returns)

    def test_sharpe_ratio_valueError_2(self):

        daily_returns = [.01]

        with self.assertRaises(ValueError):
            calculate_sharpe_ratio(daily_returns)

