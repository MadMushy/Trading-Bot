import unittest
from alpaca.common.exceptions import APIError
from alpaca.trading.enums import OrderStatus
from unittest.mock import patch, MagicMock
from decimal import Decimal
from alpaca_client import get_all_positions, create_market_order, submit_order, is_valid_uuid, get_order_by_id, get_order_by_client_id, is_order_filled, get_remaining_quantity, get_active_remaining_quantity, summarize_order, calculate_position_difference

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
        valid_id = is_valid_uuid(order.client_order_id)
        
        self.assertEqual(order.symbol, "SPY")
        self.assertEqual(order.qty, 5)
        self.assertEqual(order.side, "buy")
        self.assertEqual(order.time_in_force, "day")
        self.assertTrue(valid_id)

    def test_create_market_order_with_client_id(self):

        order = create_market_order("SPY", 5, client_order_id="test-order-001")
        valid_id = is_valid_uuid(order.client_order_id)
        
        self.assertEqual(order.symbol, "SPY")
        self.assertEqual(order.qty, 5)
        self.assertEqual(order.side, "buy")
        self.assertEqual(order.time_in_force, "day")
        self.assertEqual(order.client_order_id, "test-order-001") 
        self.assertFalse(valid_id)

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

    def test_get_order_by_client_id(self):

        client_id = "550e8400-e29b-41d4-a716-446655440000"

        fake_order = MagicMock()
        fake_order.id = "alpaca-order-123"
        fake_order.client_order_id = client_id
        fake_order.status = "pending"

        with patch("alpaca_client.trading_client.get_order_by_client_id") as mock_get_order:
            mock_get_order.return_value = fake_order

            result = get_order_by_client_id(client_id)
            self.assertEqual(result.client_order_id, client_id)
            self.assertEqual(result.status, "pending")
            self.assertEqual(result.id, "alpaca-order-123")
            mock_get_order.assert_called_once_with(client_id)

    def test_order_filled(self):
        fake_order = MagicMock()
        fake_order.status = OrderStatus.FILLED

        result = is_order_filled(fake_order)

        self.assertTrue(result)

    def test_order_not_filled(self):
        fake_order = MagicMock()
        fake_order.status = OrderStatus.PARTIALLY_FILLED

        result = is_order_filled(fake_order)

        self.assertFalse(result)

    def test_get_remaining_quantity(self):

        fake_order = MagicMock()

        fake_order.qty = "10"
        fake_order.filled_qty = "5"

        remaining_qty = get_remaining_quantity(fake_order)

        self.assertEqual(remaining_qty, Decimal("5"))
        self.assertIsInstance(remaining_qty, Decimal)

    def test_get_remaining_quantity_value_error(self):

        fake_order = MagicMock()

        fake_order.qty = "10"
        fake_order.filled_qty = "11"

        with self.assertRaises(ValueError):
            get_remaining_quantity(fake_order)

    def test_get_active_remaining_quantity_PARTIALLY_FILLED(self):

        fake_order = MagicMock()

        fake_order.status = OrderStatus.PARTIALLY_FILLED
        fake_order.qty = "10"
        fake_order.filled_qty = "4"

        remaining_qty = get_active_remaining_quantity(fake_order)

        self.assertEqual(remaining_qty, Decimal("6"))
        self.assertIsInstance(remaining_qty, Decimal)

    def test_get_active_remaining_quantity_CANCELED(self):

        fake_order = MagicMock()

        fake_order.status = OrderStatus.CANCELED
        fake_order.qty = "10"
        fake_order.filled_qty = "4"

        remaining_qty = get_active_remaining_quantity(fake_order)

        self.assertEqual(remaining_qty, Decimal("0"))
        self.assertIsInstance(remaining_qty, Decimal)

    def test_get_active_remaining_quantity_VALUEERROR(self):

        fake_order = MagicMock()

        fake_order.status = None
        fake_order.qty = "10"
        fake_order.filled_qty = "4"

        with self.assertRaises(ValueError):
            get_active_remaining_quantity(fake_order)

    def test_get_active_remaining_quantity_PENDING_CANCEL(self):

        fake_order = MagicMock()

        fake_order.status = OrderStatus.PENDING_CANCEL
        fake_order.qty = "10"
        fake_order.filled_qty = "4"

        remaining_qty = get_active_remaining_quantity(fake_order)

        self.assertEqual(remaining_qty, Decimal("6"))
        self.assertIsInstance(remaining_qty, Decimal)

    def test_get_active_remaining_quantity_ACCEPTED(self):

        fake_order = MagicMock()

        fake_order.status = OrderStatus.ACCEPTED
        fake_order.qty = "10"
        fake_order.filled_qty = "0"

        remaining_qty = get_active_remaining_quantity(fake_order)

        self.assertEqual(remaining_qty, Decimal("10"))
        self.assertIsInstance(remaining_qty, Decimal)

    def test_summarize_order_PARTIALLY_FILLED(self):

        fake_order = MagicMock()

        fake_order.status = OrderStatus.PARTIALLY_FILLED
        fake_order.qty = "10"
        fake_order.filled_qty = "4"
        fake_order.id = "alpaca-order-123"
        fake_order.client_order_id = "my-order-001"

        summary = summarize_order(fake_order)

        self.assertEqual(summary["order_id"], "alpaca-order-123")
        self.assertEqual(summary["client_order_id"], "my-order-001")
        self.assertEqual(summary["status"], OrderStatus.PARTIALLY_FILLED)
        self.assertEqual(summary["ordered_qty"], Decimal("10"))
        self.assertEqual(summary["filled_qty"], Decimal("4"))
        self.assertEqual(summary["remaining_qty"], Decimal("6"))
        self.assertEqual(summary["active_remaining_qty"], Decimal("6"))

    def test_summarize_order_CANCELED(self):

        fake_order = MagicMock()

        fake_order.status = OrderStatus.CANCELED
        fake_order.qty = "10"
        fake_order.filled_qty = "4"
        fake_order.id = "alpaca-order-123"
        fake_order.client_order_id = "my-order-001"

        summary = summarize_order(fake_order)

        self.assertEqual(summary["order_id"], "alpaca-order-123")
        self.assertEqual(summary["client_order_id"], "my-order-001")
        self.assertEqual(summary["status"], OrderStatus.CANCELED)
        self.assertEqual(summary["ordered_qty"], Decimal("10"))
        self.assertEqual(summary["filled_qty"], Decimal("4"))
        self.assertEqual(summary["remaining_qty"], Decimal("6"))
        self.assertEqual(summary["active_remaining_qty"], Decimal("0"))

    def test_position_difference_positive(self):
    
        result = calculate_position_difference("10", "4", "3", "0")
    
        self.assertEqual(result, Decimal("3"))

    def test_position_difference_negative(self):
        
        result = calculate_position_difference("4", "10", "0", "3")
    
        self.assertEqual(result, Decimal("-3"))

    def test_position_difference_zero(self):
        
        result = calculate_position_difference("10", "4", "6", "0")
    
        self.assertEqual(result, Decimal("0"))

    def test_position_difference_input_validation_target(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("-1", "4", "6", "0")

    def test_position_difference_input_validation_current(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("10", "-1", "6", "0")

    def test_position_difference_input_validation_pending_buy(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("10", "4", "-1", "0")

    def test_position_difference_input_validation_pending_sell(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("10", "4", "6", "-1")

    def test_position_difference_input_validation_target_non_finite(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("NaN", "4", "6", "0")

    def test_position_difference_input_validation_current_non_finite(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("10", "Infinity", "6", "0")

    def test_position_difference_input_validation_target_abc(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("abc", "4", "6", "0")

    def test_position_difference_input_validation_current_None(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("10", "None", "6", "0")

    def test_position_difference_input_validation_blank(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("10", "4", "", "0")

    def test_position_difference_input_validation_list(self):

        with self.assertRaises(ValueError):
            calculate_position_difference("10", "4", "6", [])
