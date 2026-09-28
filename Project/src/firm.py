class Firm:

    def __init__(self, name, marginal_cost=0):
        self.name = name
        self.marginal_cost = marginal_cost
        self.quantity = 0
        self.total_profit = 0.0
        self.history = []  # stores (quantity, profit) for each round

    def set_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity

    # profit = (price - cost) * quantity produced
    def calculate_profit(self, price):
        profit = (price - self.marginal_cost) * self.quantity
        self.total_profit += profit
        self.history.append((self.quantity, round(profit, 2)))
        return round(profit, 2)

    # reset everything for a new game
    def reset(self):
        self.quantity = 0
        self.total_profit = 0.0
        self.history = []