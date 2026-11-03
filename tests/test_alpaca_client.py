import unittest
from unittest.mock import patch, MagicMock
from alpaca_client import get_all_positions

class TestAlpacaClient(unittest.TestCase):

    def test_mock_client_call(self):

        with patch("alpaca_client.trading_client.get_all_positions") as mock_positions:
            mock_positions.return_value = []

            result = get_all_positions()

            self.assertEqual(result, [])
            mock_positions.assert_called_once_with()

    def test_client_with_positions(self):

        #Initialize Magic Mock
        fake_position = MagicMock()

        fake_position.symbol = "SPY"
        fake_position.qty = "10"
        fake_position.market_value = "6000.00"

        with patch("alpaca_client.trading_client.get_all_positions") as mock_positions:
            mock_positions.return_value = [fake_position]

            result = get_all_positions()

            self.assertEqual(result[0].symbol, "SPY")
            mock_positions.assert_called_once_with()
