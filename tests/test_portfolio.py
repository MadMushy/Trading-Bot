import unittest
from decimal import Decimal
from portfolio import calculate_strategy_target

class TestPortfolio(unittest.TestCase):
    def test_calculate_strategy_target_1(self):

        signal = "BUY"
        previous_state = "OUT"
        previous_target_qty = 0
        capital = 10000
        allocation = .95
        share_price = 500

        result = calculate_strategy_target(
                signal, 
                previous_state,
                previous_target_qty,
                capital,
                allocation, 
                share_price
        )

        self.assertEqual(result["state"], "INVESTED")
        self.assertEqual(result["target_qty"], 19)

    def test_calculate_valid_strategy_targets(self):
        capital = 10000
        allocation = .95
        
        cases = [
            ("BUY", "INVESTED", 19, 400, "INVESTED", 23),
            ("HOLD", "INVESTED", 19, 600, "INVESTED", 19),
            ("HOLD", "INVESTED", 19, 400, "INVESTED", 19),
            ("SELL", "INVESTED", 19, 600, "OUT", 0),
            ("SELL", "OUT", 0, 500, "OUT", 0),
            ("HOLD", "OUT", 0, 500, "OUT", 0),
            ("HOLD", "INVESTED", 0, 500, "INVESTED", 0)
        ]

        for signal, previous_state, previous_qty, price, expected_state, expected_qty in cases:
            with self.subTest(
                    signal=signal,
                    previous_state=previous_state,
                    previous_qty=previous_qty,
                    price=price,
                    expected_state=expected_state,
                    expected_qty=expected_qty
            ):
                result = calculate_strategy_target(
                            signal,
                            previous_state,
                            previous_qty,
                            capital,
                            allocation,
                            price
                )

                self.assertEqual(result["state"], expected_state)
                self.assertEqual(result["target_qty"], expected_qty)

    def test_calculate_in_valid_strategy_targets(self):
        capital = 10000
        allocation = .95
        
        cases = [
            ("BUY", "INVESTED", -5, 400, "INVESTED", 23),
            ("HOLD", "INVESTED", 2.5, 600, "INVESTED", 19),
            ("HOLD", "INVESTED", "19", 400, "INVESTED", 19),
            ("SELL", "INVESTED", None, 600, "OUT", 0),
            ("SELL", "OUT", True, 500, "OUT", 0),
            ("INVALID", "OUT", 0, 500, "OUT", 0),
            ("HOLD", "INVALID", 0, 500, "INVESTED", 0)
        ]

        for signal, previous_state, previous_qty, price, expected_state, expected_qty in cases:
            with self.subTest(
                    signal=signal,
                    previous_state=previous_state,
                    previous_qty=previous_qty,
                    price=price,
                    expected_state=expected_state,
                    expected_qty=expected_qty
            ):
                with self.assertRaises(ValueError): 
                    calculate_strategy_target(
                            signal,
                            previous_state,
                            previous_qty,
                            capital,
                            allocation,
                            price
                    )
