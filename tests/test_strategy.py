import unittest
from strategy import calculate_sma, generate_signal, update_strategy_state

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

    def test_update_strategy_state_1(self):
        signal = "BUY"
        previous_state = "OUT"

        result = update_strategy_state(signal, previous_state)

        self.assertEqual(result, "INVESTED")

    def test_update_strategy_state_2(self):
        signal = "BUY"
        previous_state = "INVESTED"

        result = update_strategy_state(signal, previous_state)

        self.assertEqual(result, "INVESTED")

    def test_update_strategy_state_3(self):
        signal = "SELL"
        previous_state = "INVESTED"

        result = update_strategy_state(signal, previous_state)

        self.assertEqual(result, "OUT")

    def test_update_strategy_state_4(self):
        signal = "SELL"
        previous_state = "OUT"

        result = update_strategy_state(signal, previous_state)

        self.assertEqual(result, "OUT")

    def test_update_strategy_state_5(self):
        signal = "HOLD"
        previous_state = "INVESTED"

        result = update_strategy_state(signal, previous_state)

        self.assertEqual(result, "INVESTED")

    def test_update_strategy_state_6(self):
        signal = "HOLD"
        previous_state = "OUT"

        result = update_strategy_state(signal, previous_state)

        self.assertEqual(result, "OUT")

    def test_update_strategy_state_valuerror_1(self):
        signal = "INVALID"
        previous_state = "OUT"

        with self.assertRaises(ValueError):
            update_strategy_state(signal, previous_state)

    def test_update_strategy_state_valuerror_2(self):
        signal = "HOLD"
        previous_state = "INVALID"

        with self.assertRaises(ValueError):
            update_strategy_state(signal, previous_state)
