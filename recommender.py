class Recommender:
    def __init__(self, symbol_data):
        self.symbol_data = symbol_data

    def recommendation(self):
        return (
            self.is_large_cap()
            and self.has_healthy_current_ratio()
            and self.has_consistent_earnings()
            and self.has_earnings_growth()
            and self.has_low_p_e_ratio()
        )

    def is_large_cap(self):
        return self.symbol_data.market_cap > 30000000000

    def has_healthy_current_ratio(self):
        return (
            self.symbol_data.current_ratio >= 1.5
            and self.symbol_data.current_ratio <= 3
        )

    def has_consistent_earnings(self):
        return all(eps >= 0 for eps in self.symbol_data.decade_of_annual_earnings)

    def has_earnings_growth(self):
        return self.symbol_data.earnings_growth_past_decade >= 0.33

    def has_low_p_e_ratio(self):
        return self.symbol_data.p_e_ratio <= 15.0
