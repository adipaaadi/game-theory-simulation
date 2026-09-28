import unittest
import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, os.path.abspath(src_path))

from game_controller import GameController


class TestGameController(unittest.TestCase):

    def setUp(self):
        # use end_probability=0 so the game never ends randomly during tests
        self.controller = GameController(end_probability=0)

    def test_round_increments(self):
        self.controller.play_round(20)
        self.assertEqual(self.controller.round, 1)

    def test_price_in_result(self):
        result = self.controller.play_round(20)
        self.assertIn("price", result)
        self.assertGreaterEqual(result["price"], 0)

    def test_player_profit_in_result(self):
        result = self.controller.play_round(20)
        self.assertIn("player_profit", result)

    def test_game_not_over_with_zero_probability(self):
        self.controller.play_round(20)
        self.assertFalse(self.controller.game_over)

    def test_reset_clears_history(self):
        self.controller.play_round(20)
        self.controller.reset()
        self.assertEqual(self.controller.round, 0)
        self.assertEqual(len(self.controller.history), 0)

    def test_save_results_creates_file(self):
        self.controller.play_round(20)
        self.controller.save_results("test_output.txt")
        self.assertTrue(os.path.exists("test_output.txt"))
        os.remove("test_output.txt")  # clean up after test


if __name__ == "__main__":
    unittest.main()