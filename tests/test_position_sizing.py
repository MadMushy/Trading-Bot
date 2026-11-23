import unittest
from decimal import Decimal
from position_sizing import calculate_target_shares

class TestPositionSizing(unittest.TestCase):
    def test_calculate_target_shares_allocation_point95(self):

        capital = 10000
        allocation = .95
        share_price = 500

        result = calculate_target_shares(capital, allocation, share_price)
        self.assertEqual(result, Decimal("19"))

    def test_calculate_target_shares_allocation_1(self):

        capital = 10000
        allocation = 1
        share_price = 600

        result = calculate_target_shares(capital, allocation, share_price)
        self.assertEqual(result, Decimal("16"))

    def test_calculate_target_shares_allocation_point5(self):

        capital = 10000
        allocation = .5
        share_price = 300

        result = calculate_target_shares(capital, allocation, share_price)
        self.assertEqual(result, Decimal("16"))

    def test_calculate_target_shares_capital_100(self):

        capital = 100
        allocation = .95
        share_price = 500

        result = calculate_target_shares(capital, allocation, share_price)
        self.assertEqual(result, Decimal("0"))

    def test_calculate_target_shares_allocation_0(self):

        capital = 10000
        allocation = 0
        share_price = 500

        result = calculate_target_shares(capital, allocation, share_price)
        self.assertEqual(result, Decimal("0"))

    def test_calculate_target_shares_capital_valueerror(self):

        capital = -100
        allocation = .95
        share_price = 500

        with self.assertRaises(ValueError):
            calculate_target_shares(capital, allocation, share_price)

    def test_calculate_target_shares_allocation_valueerror(self):

        capital = 100
        allocation = 1.5
        share_price = 500

        with self.assertRaises(ValueError):
            calculate_target_shares(capital, allocation, share_price)

    def test_calculate_target_shares_share_price_valueerror(self):

        capital = 100
        allocation = .95
        share_price = 0

        with self.assertRaises(ValueError):
            calculate_target_shares(capital, allocation, share_price)

    def test_calculate_target_shares_finite_valueerror(self):

        capital = 100
        allocation = .95
        share_price = "NaN"

        with self.assertRaises(ValueError):
            calculate_target_shares(capital, allocation, share_price)






