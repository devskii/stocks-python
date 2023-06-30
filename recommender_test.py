import unittest
from recommender import Recommender
from symbol_data import SymbolData
from unittest.mock import MagicMock


class TestRecommender(unittest.TestCase):
    def test_large_cap(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.market_cap = 30000000001
        recommender = Recommender(mock_symbol_data)
        self.assertTrue(recommender.is_large_cap())

    def test_not_large_cap(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.market_cap = 29999999999
        recommender = Recommender(mock_symbol_data)
        self.assertFalse(recommender.is_large_cap())

    def test_has_healthy_current_ratio(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.current_ratio = 2.0
        recommender = Recommender(mock_symbol_data)
        self.assertTrue(recommender.has_healthy_current_ratio())

    def test_has_unhealthy_high_current_ratio(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.current_ratio = 3.001
        recommender = Recommender(mock_symbol_data)
        self.assertFalse(recommender.has_healthy_current_ratio())

    def test_has_unhealthy_low_current_ratio(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.current_ratio = 1.499
        recommender = Recommender(mock_symbol_data)
        self.assertFalse(recommender.has_healthy_current_ratio())

    def test_has_consistent_earnings(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.decade_of_annual_earnings = [0.1] * 10
        recommender = Recommender(mock_symbol_data)
        self.assertTrue(recommender.has_consistent_earnings())

    def test_has_inconsistent_earnings(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.decade_of_annual_earnings = [-0.1] + [0.1] * 9
        recommender = Recommender(mock_symbol_data)
        self.assertFalse(recommender.has_consistent_earnings())

    def test_has_earnings_growth(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.earnings_growth_past_decade = 0.33
        recommender = Recommender(mock_symbol_data)
        self.assertTrue(recommender.has_earnings_growth())

    def test_has_insufficient_earnings_growth(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.earnings_growth_past_decade = 0.32
        recommender = Recommender(mock_symbol_data)
        self.assertFalse(recommender.has_earnings_growth())

    def test_has_low_p_e_ratio(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.p_e_ratio = 15.0
        recommender = Recommender(mock_symbol_data)
        self.assertTrue(recommender.has_low_p_e_ratio())

    def test_has_high_p_e_ratio(self):
        mock_symbol_data = MagicMock(SymbolData)
        mock_symbol_data.p_e_ratio = 15.1
        recommender = Recommender(mock_symbol_data)
        self.assertFalse(recommender.has_low_p_e_ratio())
