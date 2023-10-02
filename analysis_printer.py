from recommender import Recommender


class AnalysisPrinter:
    def __init__(self, symbol_data):
        self.symbol_data = symbol_data
        self.recommender = Recommender(symbol_data)

    def print_analysis(self):
        self.print_recommendation()
        self.print_criteria()
        self.print_details()
        print("============================")

    def print_recommendation(self):
        print("====== RECOMMENDATION ======")
        print(
            f"The recommendation for {self.symbol_data.symbol} is {self.recommender.recommendation()}"
        )

    def print_criteria(self):
        print("--------- Criteria ---------")
        print(f"is_large_cap: {self.recommender.is_large_cap()}")
        print(
            f"has_healthy_current_ratio: {self.recommender.has_healthy_current_ratio()}"
        )
        print(f"has_consistent_earnings: {self.recommender.has_consistent_earnings()}")
        print(f"has_earnings_growth: {self.recommender.has_earnings_growth()}")
        print(f"has_low_pe_ratio: {self.recommender.has_low_p_e_ratio()}")

    def print_details(self):
        print("--------- Details ----------")
        print(f"Market Cap: {format(self.symbol_data.market_cap, ',')}")
        print(f"Current Ratio: {round(self.symbol_data.current_ratio, 2)}")
        print(f"10 years of Annual EPS (going back in time): {self.symbol_data.decade_of_annual_earnings}")
        print(
            f"Earnings Growth over last decade: {round(self.symbol_data.earnings_growth_past_decade * 100, 0)}%"
        )
        print(
            f"P/E Ratio based on most recent 12 quarters: {round(self.symbol_data.p_e_ratio, 2)}"
        )
        print(f"Market Price: ${self.symbol_data.market_price}")
