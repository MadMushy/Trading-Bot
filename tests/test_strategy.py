import unittest
from strategy import calculate_sma, generate_signal

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

	def test_buy_signal(self):
		prices = [100] * 20 + [110]
		result = generate_signal(prices)
		self.assertEqual(result, "BUY")

	def test_sell_signal(self):
		prices = [100] * 20 + [99]
		result = generate_signal(prices)
		self.assertEqual(result, "SELL")

	def test_hold_signal(self):
		prices = [100] * 21
		result = generate_signal(prices)
		self.assertEqual(result, "HOLD")
