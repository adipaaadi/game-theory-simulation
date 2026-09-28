import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from firm import Firm


class TestFirm(unittest.TestCase):

    def setUp(self):
        self.firm = Firm("Player", marginal_cost=0)

    def test_initial_profit_is_zero(self):
        self.assertEqual(self.firm.total_profit, 0)

    def test_profit_calculation(self):
        self.firm.set_quantity(10)
        profit = self.firm.calculate_profit(50)
        # (50 - 0) * 10 = 500
        self.assertEqual(profit, 500)

    def test_profit_accumulates(self):
        self.firm.set_quantity(10)
        self.firm.calculate_profit(50)
        self.firm.set_quantity(10)
        self.firm.calculate_profit(40)
        self.assertEqual(self.firm.total_profit, 900)

    def test_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.firm.set_quantity(-5)

    def test_reset_clears_state(self):
        self.firm.set_quantity(10)
        self.firm.calculate_profit(50)
        self.firm.reset()
        self.assertEqual(self.firm.total_profit, 0)
        self.assertEqual(len(self.firm.history), 0)


if __name__ == "__main__":
    unittest.main()