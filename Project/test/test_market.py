import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from market import Market


class TestMarket(unittest.TestCase):

    def setUp(self):
        self.market = Market(a=100, b=1)

    # when nothing is produced price should just be the intercept
    def test_price_zero_production(self):
        price = self.market.get_price(0, 0)
        self.assertEqual(price, 100)

    # more production = lower price
    def test_price_decreases_with_quantity(self):
        price_low = self.market.get_price(10, 10)
        price_high = self.market.get_price(30, 30)
        self.assertGreater(price_low, price_high)

    # price should never go negative
    def test_price_not_negative(self):
        price = self.market.get_price(200, 200)
        self.assertGreaterEqual(price, 0)

    # with a=100, b=1, c=0 each firm should produce ~33.33 at equilibrium
    def test_nash_equilibrium(self):
        eq = self.market.get_nash_equilibrium(marginal_cost=0)
        self.assertAlmostEqual(eq["quantity_each"], 33.33, places=1)


if __name__ == "__main__":
    unittest.main()