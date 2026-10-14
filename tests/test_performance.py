import unittest
from performance import calculate_return, calculate_max_drawdown


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

