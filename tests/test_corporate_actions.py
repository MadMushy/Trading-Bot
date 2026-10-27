import unittest

from corporate_actions import calculate_dividend_payment, record_dividend_entitlement, process_dividend_payments

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
        pending_dividends = []

        pending_dividends = record_dividend_entitlement(pending_dividends, shares, dividend_per_share, payment_date)

        self.assertEqual(len(pending_dividends), 1)
        self.assertAlmostEqual(pending_dividends[0]["amount"], 87.50)
        self.assertEqual(pending_dividends[0]["payment_date"], "2026-06-30")

    def test_dividend_entitlement_2(self):

        shares = 0
        dividend_per_share = 1.75
        payment_date = "2026-06-30"
        pending_dividends = []

        pending_dividends = record_dividend_entitlement(pending_dividends, shares, dividend_per_share, payment_date)

        self.assertEqual(len(pending_dividends), 0)

    def test_dividend_entitlement_2(self):

        shares = 50
        dividend_per_share = 1.75
        payment_date = "2026-06-30"
        pending_dividends = []

        pending_dividends = record_dividend_entitlement(pending_dividends, shares, dividend_per_share, payment_date)

        pending_dividends = record_dividend_entitlement(pending_dividends, shares, dividend_per_share, payment_date)

        self.assertEqual(len(pending_dividends), 2)

    def test_process_dividend_payments_2_payments(self):

        pending_dividends = [
            {"payment_date": "2026-06-30", "amount": 87.50},
            {"payment_date": "2026-09-30", "amount": 90.00}
        ]
        cash = 1000
        current_date = "2026-10-20"

        cash, updated_dividends = process_dividend_payments(pending_dividends, current_date, cash)

        self.assertAlmostEqual(cash, 1177.50)
        self.assertEqual(len(updated_dividends), 0)

    def test_process_dividend_payments_1_payment(self):

        pending_dividends = [{"payment_date": "2026-06-30", "amount": 87.50}]
        cash = 1000
        current_date = "2026-10-20"

        cash, remaining = process_dividend_payments(pending_dividends, current_date, cash)

        self.assertAlmostEqual(cash, 1087.50)
        self.assertAlmostEqual(len(remaining), 0)

    def test_process_dividend_payments_future_payment(self):

        pending_dividends = [{"payment_date": "2026-06-30", "amount": 87.50}]
        cash = 1000
        current_date = "2026-06-20"

        cash, remaining = process_dividend_payments(pending_dividends, current_date, cash)

        self.assertAlmostEqual(cash, 1000)
        self.assertAlmostEqual(len(remaining), 1)

    def test_process_dividend_payments_1_payment_1_future(self):

        pending_dividends = [
            {"payment_date": "2026-06-30", "amount": 87.50},
            {"payment_date": "2026-09-30", "amount": 90.00}
        ]
        cash = 1000
        current_date = "2026-08-20"

        cash, updated_dividends = process_dividend_payments(pending_dividends, current_date, cash)

        self.assertAlmostEqual(cash, 1087.50)
        self.assertEqual(len(updated_dividends), 1)


