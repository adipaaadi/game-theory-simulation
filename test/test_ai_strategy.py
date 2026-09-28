import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from market import Market
from ai_strategy import AIStrategy


class TestAIStrategy(unittest.TestCase):

    def setUp(self):
        self.market = Market(a=100, b=1)
        self.ai = AIStrategy(self.market)

    def test_first_move_is_nash_quantity(self):
        # with no history AI should play Nash eq quantity (~33)
        q = self.ai.decide([])
        self.assertAlmostEqual(q, 33, delta=1)

    def test_best_response_to_high_quantity(self):
        # if player produces a lot, AI should produce less
        history = [{"player_quantity": 80, "ai_quantity": 33}]
        q = self.ai.decide(history)
        self.assertLess(q, 33)

    def test_quantity_never_negative(self):
        # even if player produces way too much, AI qty should stay >= 0
        history = [{"player_quantity": 200, "ai_quantity": 0}]
        q = self.ai.decide(history)
        self.assertGreaterEqual(q, 0)


if __name__ == "__main__":
    unittest.main()