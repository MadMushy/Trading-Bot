import unittest
from decimal import Decimal
from portfolio import calculate_strategy_target

class TestPortfolio(unittest.TestCase):
    def test_calculate_strategy_target_1(self):

        signal = "BUY"
        previous_state = "OUT"
        capital = 10000
        allocation = .95
        share_price = 500

        result = calculate_strategy_target(
                signal, 
                previous_state,
                capital,
                allocation, 
                share_price
        )


