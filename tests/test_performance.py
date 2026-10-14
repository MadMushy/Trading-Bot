import unittest
from performance import calculate_return


class TestPerformance(unittest.TestCase):

    def test_positive_return(self):

        result = calculate_return(10000, 12000)
        self.assertEqual(result, 20.0)

    def test_negative_return(self):

        result = calculate_return(10000, 8200)
        self.assertEqual(result, -18.0)

    def test_zero_return(self):

        result = calculate_return(10000, 10000)
        self.assertEqual(result, 0.0)

    def test_value_error(self):

        with self.assertRaises(ValueError):
            calculate_return(-10000, 12000)

