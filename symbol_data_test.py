import unittest
from symbol_data import SymbolData


symbol = "FOO"
overview = {"MarketCapitalization": 30000000001}
balance_sheet = {
    "quarterlyReports": [{"totalCurrentAssets": 2000, "totalCurrentLiabilities": 1000}]
}
earnings = {
    "annualEarnings": [{"reportedEPS": 1.33}] * 3 + [{"reportedEPS": 1.0}] * 7,
    "quarterlyEarnings": [{"reportedEPS": 1.0}] * 12,
}
quote = {
    "Global Quote": {"05. price": "60.00"},
}


class TestSymbolData(unittest.TestCase):
    def test_market_cap(self):
        symbol_data = SymbolData(
            symbol,
            overview,
            balance_sheet,
            earnings,
            quote,
            time_series_monthly_adjusted=None,
        )
        self.assertEqual(30000000001, symbol_data.market_cap)

    def test_current_ratio(self):
        symbol_data = SymbolData(
            symbol,
            overview,
            balance_sheet,
            earnings,
            quote,
            time_series_monthly_adjusted=None,
        )
        self.assertEqual(2.0, symbol_data.current_ratio)

    def test_decade_of_annual_earnings(self):
        symbol_data = SymbolData(
            symbol,
            overview,
            balance_sheet,
            earnings,
            quote,
            time_series_monthly_adjusted=None,
        )
        self.assertEqual([1.33] * 3 + [1.0] * 7, symbol_data.decade_of_annual_earnings)

    def test_earnings_growth_past_decade(self):
        symbol_data = SymbolData(
            symbol,
            overview,
            balance_sheet,
            earnings,
            quote,
            time_series_monthly_adjusted=None,
        )
        self.assertAlmostEqual(0.33, symbol_data.earnings_growth_past_decade)

    def test_p_e_ratio(self):
        symbol_data = SymbolData(
            symbol,
            overview,
            balance_sheet,
            earnings,
            quote,
            time_series_monthly_adjusted=None,
        )
        self.assertEqual(15.0, symbol_data.p_e_ratio)
