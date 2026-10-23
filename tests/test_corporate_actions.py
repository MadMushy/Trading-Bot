import unittest

from corporate_actions import calculate_dividend_payment

class TestCorporateActions(unittest.TestCase):
    def test_corporate_actions_1(self):

        shares = 50
        dividend_per_share = 1.75

        payment = calculate_dividend_payment(shares, dividend_per_share)

        self.assertAlmostEqual(payment, 87.50)

    def test_corporate_actions_2(self):

        shares = 0
        dividend_per_share = 2.0

        payment = calculate_dividend_payment(shares, dividend_per_share)

        self.assertEqual(payment, 0)

    def test_corporate_actions_negative_shares(self):

        shares = -5
        dividend_per_share = 1.75

        with self.assertRaises(ValueError):
            calculate_dividend_payment(shares, dividend_per_share)

    def test_dividend_entitlement_1(self):

        shares = 50
        dividend_per_share = 1.75
        payment_date = "2026-06-30"




