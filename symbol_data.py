class SymbolData:
    def __init__(
        self,
        symbol,
        overview,
        balance_sheet,
        earnings,
        quote,
        time_series_monthly_adjusted,
    ):
        self.symbol = symbol
        self.time_series_monthly_adjusted = time_series_monthly_adjusted

        # set market_cap
        self.market_cap = int(overview["MarketCapitalization"])

        # set current_ratio
        quarterly_reports = balance_sheet["quarterlyReports"]
        total_current_assets = int(quarterly_reports[0]["totalCurrentAssets"])
        total_current_liabilities = int(quarterly_reports[0]["totalCurrentLiabilities"])
        self.current_ratio = total_current_assets / total_current_liabilities

        # set decade_of_annual_earnings
        self.decade_of_annual_earnings = [
            float(year["reportedEPS"]) for year in earnings["annualEarnings"][:10]
        ]

        # set earnings_growth_past_decade
        most_recent_three_years = sum(self.decade_of_annual_earnings[:3])
        decade_beginning_three_years = sum(self.decade_of_annual_earnings[7:10])
        difference = most_recent_three_years - decade_beginning_three_years
        self.earnings_growth_past_decade = difference / decade_beginning_three_years

        # set p_e_ratio
        quarterly_earnings = earnings["quarterlyEarnings"]
        recent_quarters_earnings = [
            float(quarter["reportedEPS"]) for quarter in quarterly_earnings[:12]
        ]
        average_annual_earnings = sum(recent_quarters_earnings) / 3
        price = float(quote["Global Quote"]["05. price"])
        self.p_e_ratio = price / average_annual_earnings
