import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from market import Market
from firm import Firm
from ai_strategy import AIStrategy


class GameController:

    def __init__(self, end_probability=0.2):
        self.market = Market(a=100, b=1)
        self.player = Firm("Player")
        self.ai = Firm("AI")
        self.ai_strategy = AIStrategy(self.market)
        self.round = 0
        self.game_over = False
        # chance the game ends after each round
        self.end_probability = end_probability
        self.history = []

    def play_round(self, player_quantity):
        if self.game_over:
            return None

        self.round += 1
        ai_quantity = self.ai_strategy.decide(self.history)

        self.player.set_quantity(player_quantity)
        self.ai.set_quantity(ai_quantity)

        price = self.market.get_price(player_quantity, ai_quantity)
        player_profit = self.player.calculate_profit(price)
        ai_profit = self.ai.calculate_profit(price)

        result = {
            "round": self.round,
            "player_quantity": player_quantity,
            "ai_quantity": ai_quantity,
            "price": round(price, 2),
            "player_profit": player_profit,
            "ai_profit": ai_profit
        }
        self.history.append(result)

        # random game end check
        if random.random() < self.end_probability:
            self.game_over = True

        return result

    def get_equilibrium(self):
        return self.market.get_nash_equilibrium()

    def get_summary(self):
        # returns end of game stats for display
        if len(self.history) == 0:
            return {}
        avg_player_q = round(
            sum(r["player_quantity"] for r in self.history) / len(self.history), 2
        )
        avg_ai_q = round(
            sum(r["ai_quantity"] for r in self.history) / len(self.history), 2
        )
        eq = self.get_equilibrium()
        return {
            "rounds": self.round,
            "player_total_profit": round(self.player.total_profit, 2),
            "ai_total_profit": round(self.ai.total_profit, 2),
            "avg_player_quantity": avg_player_q,
            "avg_ai_quantity": avg_ai_q,
            "eq_quantity": eq["quantity_each"],
            "eq_price": eq["price"]
        }

    def save_results(self, filepath="results.txt"):
        # saves round-by-round results and final summary to a text file
        s = self.get_summary()
        with open(filepath, "w") as f:
            f.write("Game Theory Simulation - Results\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Total rounds: {s['rounds']}\n\n")
            f.write(f"{'Round':<8}{'Your Qty':<12}{'AI Qty':<12}{'Price':<12}{'Your Profit'}\n")
            f.write("-" * 55 + "\n")
            for r in self.history:
                f.write(
                    f"{r['round']:<8}{r['player_quantity']:<12}{r['ai_quantity']:<12}"
                    f"{r['price']:<12}{r['player_profit']}\n"
                )
            f.write("\n" + "=" * 40 + "\n")
            f.write(f"Your total profit:  {s['player_total_profit']}\n")
            f.write(f"AI total profit:    {s['ai_total_profit']}\n")
            f.write(f"Your avg quantity:  {s['avg_player_quantity']}\n")
            f.write(f"Nash eq. quantity:  {s['eq_quantity']}\n")
            f.write(f"Nash eq. price:     {s['eq_price']}\n")

    def reset(self):
        self.player.reset()
        self.ai.reset()
        self.round = 0
        self.game_over = False
        self.history = []