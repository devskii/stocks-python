import unittest
from foo_symbol_data import FOO_SYMBOL_DATA


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
