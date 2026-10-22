import unittest

from corporate_actions import calculate_dividend_payment

class TestCorporateActions(unittest.TestCase):
    def test_corporate_actions_1(self):

        shares = 50
        dividend_per_share = 1.75

        payment = calculate_dividend_payment(shares, dividend_per_share)

        self.assertAlmostEqual(payment, 87.50)


