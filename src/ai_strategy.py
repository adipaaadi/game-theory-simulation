class AIStrategy:

    def __init__(self, market):
        self.market = market

    def decide(self, history):
        if len(history) == 0:
            return round(self.market.get_nash_equilibrium()["quantity_each"])

        last_player_q = history[-1]["player_quantity"]
        q_ai = (self.market.a - self.market.b * last_player_q) / (2 * self.market.b)
        return max(0, round(q_ai))