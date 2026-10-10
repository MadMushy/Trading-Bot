import unittest
from strategy import calculate_sma

class TestSMA(unittest.TestCase):

	def test_valid_sma(self):
		prices = [100, 105, 110, 115, 120]

		result = calculate_sma(prices, 3)

		self.assertAlmostEqual(result, 115)

	def test_period_too_large(self):
		prices = [100, 105, 110]

		with self.assertRaises(ValueError):
			calculate_sma(prices, 10)

	def test_zero_period(self):
		prices = [100, 105, 110]

		with self.assertRaises(ValueError):
			calculate_sma(prices, 0)
