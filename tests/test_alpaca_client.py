import unittest
from unittest.mock import patch
from alpaca_client import get_all_positions

class TestAlpacaClient(unittest.TestCase):

    def test_mock_client_call(self):

        with patch("alpaca_client.trading_client.get_all_positions") as mock_positions:
            mock_positions.return_value = []

            result = get_all_positions()

            self.assertEqual(result, [])
