import unittest

from symbol_data import SymbolData

SYMBOL = "FOO"
OVERVIEW = {"MarketCapitalization": 30000000001}
BALANCE_SHEET = {
    "quarterlyReports": [{"totalCurrentAssets": 2000, "totalCurrentLiabilities": 1000}]
}
EARNINGS = {
    "annualEarnings": [{"reportedEPS": 1.33}] * 3 + [{"reportedEPS": 1.0}] * 7,
    "quarterlyEarnings": [{"reportedEPS": 1.0}] * 12,
}
QUOTE = {
    "Global Quote": {"05. price": "60.00"},
}
FOO_SYMBOL_DATA = SymbolData(
    SYMBOL,
    OVERVIEW,
    BALANCE_SHEET,
    EARNINGS,
    QUOTE,
    time_series_monthly_adjusted=None,
)


class TestSymbolData(unittest.TestCase):
    def test_market_cap(self):
        self.assertEqual(30000000001, FOO_SYMBOL_DATA.market_cap)

    def test_current_ratio(self):
        self.assertEqual(2.0, FOO_SYMBOL_DATA.current_ratio)

    def test_decade_of_annual_earnings(self):
        self.assertEqual(
            [1.33] * 3 + [1.0] * 7, FOO_SYMBOL_DATA.decade_of_annual_earnings
        )

    def test_earnings_growth_past_decade(self):
        self.assertAlmostEqual(0.33, FOO_SYMBOL_DATA.earnings_growth_past_decade)

    def test_p_e_ratio(self):
        self.assertEqual(15.0, FOO_SYMBOL_DATA.p_e_ratio)
