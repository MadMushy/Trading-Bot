import unittest

from corporate_actions import calculate_dividend_payment, record_dividend_entitlement, process_dividend_payments, apply_stock_split, adjust_prices_for_splits
from datetime import date, timedelta

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

    def test_dividend_entitlement_3(self):

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

    def test_stock_split(self):

        result = apply_stock_split(25,5)

        self.assertEqual(result, 125)

    def test_adjust_prices_for_splits(self):

        prices = [200, 200, 200, 100, 100]
        start_date = date(2026, 10, 1)
        dates = [
        (start_date + timedelta(days=i)).isoformat()
        for i in range(len(prices))
        ]
        split_events = [
            {
                "ex_date": dates[3],
                "split_ratio": 2.0

            }
        ]
       
        result = adjust_prices_for_splits(
                prices=prices,
                dates=dates,
                split_events=split_events
            )

        print(result)
        self.assertEqual(result[0], 100)

    def test_adjust_prices_for_splits_multiple(self):

        prices = [400, 400, 200, 200, 50]
        start_date = date(2026, 10, 1)
        dates = [
        (start_date + timedelta(days=i)).isoformat()
        for i in range(len(prices))
        ]
        split_events = [
            {
                "ex_date": dates[2],
                "split_ratio": 2

            },
            {
                "ex_date": dates[4],
                "split_ratio": 4
            }
        ]
       
        result = adjust_prices_for_splits(
                prices=prices,
                dates=dates,
                split_events=split_events
            )

        print(result)
        self.assertEqual(result[0], 50)
