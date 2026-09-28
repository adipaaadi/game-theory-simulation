class Market:
    # a = demand, b = slope of demand curve
    def __init__(self, a=100, b=1):
        self.a = a
        self.b = b

    def get_price(self, q1, q2):
        total = q1 + q2
        price = self.a - self.b * total
        if price < 0:
            price = 0
        return price
    
    # formula: q* = (a - c) / (3b)
    def get_nash_equilibrium(self, marginal_cost=0):
        q_star = (self.a - marginal_cost) / (3 * self.b)
        p_star = self.a - self.b * 2 * q_star
        return {
            "quantity_each": round(q_star, 2),
            "price": round(p_star, 2)
        }