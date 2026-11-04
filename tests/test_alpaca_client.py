import unittest
from alpaca.common.exceptions import APIError
from unittest.mock import patch, MagicMock
from alpaca_client import get_all_positions, create_market_order, submit_order, is_valid_uuid, get_order_by_id 

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

    def test_create_market_order(self):

        order = create_market_order("SPY", 5)

        self.assertEqual(order.symbol, "SPY")
        self.assertEqual(order.qty, 5)
        self.assertEqual(order.side, "buy")
        self.assertEqual(order.time_in_force, "day")

    def test_creat_markey_order_valueerror(self):

        with self.assertRaises(ValueError):
            create_market_order("SPY", 0)

    def test_client_submit_order(self):

        order_request = create_market_order("SPY", 5)

        fake_position = MagicMock()

        fake_position.id = "test-order-123"
        fake_position.status = "accepted"

        with patch("alpaca_client.trading_client.submit_order") as mock_positions:
            mock_positions.return_value = fake_position

            order = submit_order(order_request)

            self.assertEqual(fake_position.id, order.id)
            self.assertEqual(order.id, "test-order-123")
            mock_positions.assert_called_once_with(order_data=order_request)

    def test_is_valid_uuid(self):

        order_id_valid = "550e8400-e29b-41d4-a716-446655440000"
        order_id_not_valid = "27855430"

        result_valid = is_valid_uuid(order_id_valid)
        result_not_valid = is_valid_uuid(order_id_not_valid)

        self.assertTrue(result_valid)
        self.assertFalse(result_not_valid)

    def test_get_order_by_id(self):

        order_id = "550e8400-e29b-41d4-a716-446655440000"

        fake_order = MagicMock()
        fake_order.id = order_id
        fake_order.status = "filled"

        with patch("alpaca_client.trading_client.get_order_by_id") as mock_get_order:
            mock_get_order.return_value = fake_order

            result = get_order_by_id(order_id)
            self.assertEqual(result.id, order_id)
            self.assertEqual(result.status, "filled")
            mock_get_order.assert_called_once_with(order_id)

    def test_get_order_by_id_invalid_uuid(self):

        order_id = "550e8400-e29b-41d4-a716-446655440000"

        fake_order = MagicMock()
        fake_order.id = order_id
        fake_order.status = "filled"

        with patch("alpaca_client.trading_client.get_order_by_id") as mock_get_order:
            mock_get_order.return_value = fake_order
        with self.assertRaises(ValueError):
            get_order_by_id("not-a-valid-uuid")

        mock_get_order.assert_not_called()

    def test_get_order_by_id_api_error(self):
        order_id = "550e8400-e29b-41d4-a716-446655440000"

        with patch("alpaca_client.trading_client.get_order_by_id") as mock_get_order:
            mock_get_order.side_effect = APIError("Order not found")

            with self.assertRaises(APIError):
                get_order_by_id(order_id)

        mock_get_order.assert_called_once_with(order_id)



