import unittest
from unittest.mock import Mock
import api
from symbol_data import SymbolData


foo = "FOO"


class TestSymbolData(unittest.TestCase):
    def setUp(self):
        overview = {"MarketCapitalization": 30000000001}
        balance_sheet = {
            "quarterlyReports": [
                {"totalCurrentAssets": 2000, "totalCurrentLiabilities": 1000}
            ]
        }
        earnings = {
            "annualEarnings": [{"reportedEPS": 1.33}] * 3 + [{"reportedEPS": 1.0}] * 7,
            "quarterlyEarnings": [{"reportedEPS": 1.0}] * 12,
        }
        quote = {
            "Global Quote": {"05. price": "60.00"},
        }

        mocked_overview = Mock()
        mocked_overview.return_value = overview
        api.get_stock_overview = mocked_overview

        mocked_balance_sheet = Mock()
        mocked_balance_sheet.return_value = balance_sheet
        api.get_stock_balance_sheet = mocked_balance_sheet

        mocked_earnings = Mock()
        mocked_earnings.return_value = earnings
        api.get_stock_earnings = mocked_earnings

        mocked_quote = Mock()
        mocked_quote.return_value = quote
        api.get_stock_quote = mocked_quote

    def test_market_cap(self):
        symbol_data = SymbolData(foo)
        self.assertEqual(30000000001, symbol_data.market_cap)

    def test_current_ratio(self):
        symbol_data = SymbolData(foo)
        self.assertEqual(2.0, symbol_data.current_ratio)

    def test_decade_of_annual_earnings(self):
        symbol_data = SymbolData(foo)
        self.assertEqual([1.33] * 3 + [1.0] * 7, symbol_data.decade_of_annual_earnings)

    def test_earnings_growth_past_decade(self):
        symbol_data = SymbolData(foo)
        self.assertAlmostEqual(0.33, symbol_data.earnings_growth_past_decade)

    def test_p_e_ratio(self):
        symbol_data = SymbolData(foo)
        self.assertEqual(15.0, symbol_data.p_e_ratio)
