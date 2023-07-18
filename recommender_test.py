import unittest
from unittest.mock import MagicMock

from recommender import Recommender
from symbol_data import SymbolData


class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.mock_symbol_data = MagicMock(SymbolData)

    def test_large_cap(self):
        self.mock_symbol_data.market_cap = 30000000001
        recommender = Recommender(self.mock_symbol_data)
        self.assertTrue(recommender.is_large_cap())

    def test_not_large_cap(self):
        self.mock_symbol_data.market_cap = 29999999999
        recommender = Recommender(self.mock_symbol_data)
        self.assertFalse(recommender.is_large_cap())

    def test_has_healthy_current_ratio(self):
        self.mock_symbol_data.current_ratio = 2.0
        recommender = Recommender(self.mock_symbol_data)
        self.assertTrue(recommender.has_healthy_current_ratio())

    def test_has_unhealthy_high_current_ratio(self):
        self.mock_symbol_data.current_ratio = 3.001
        recommender = Recommender(self.mock_symbol_data)
        self.assertFalse(recommender.has_healthy_current_ratio())

    def test_has_unhealthy_low_current_ratio(self):
        self.mock_symbol_data.current_ratio = 1.499
        recommender = Recommender(self.mock_symbol_data)
        self.assertFalse(recommender.has_healthy_current_ratio())

    def test_has_consistent_earnings(self):
        self.mock_symbol_data.decade_of_annual_earnings = [0.1] * 10
        recommender = Recommender(self.mock_symbol_data)
        self.assertTrue(recommender.has_consistent_earnings())

    def test_has_inconsistent_earnings(self):
        self.mock_symbol_data.decade_of_annual_earnings = [-0.1] + [0.1] * 9
        recommender = Recommender(self.mock_symbol_data)
        self.assertFalse(recommender.has_consistent_earnings())

    def test_has_earnings_growth(self):
        self.mock_symbol_data.earnings_growth_past_decade = 0.33
        recommender = Recommender(self.mock_symbol_data)
        self.assertTrue(recommender.has_earnings_growth())

    def test_has_insufficient_earnings_growth(self):
        self.mock_symbol_data.earnings_growth_past_decade = 0.32
        recommender = Recommender(self.mock_symbol_data)
        self.assertFalse(recommender.has_earnings_growth())

    def test_has_low_p_e_ratio(self):
        self.mock_symbol_data.p_e_ratio = 15.0
        recommender = Recommender(self.mock_symbol_data)
        self.assertTrue(recommender.has_low_p_e_ratio())

    def test_has_high_p_e_ratio(self):
        self.mock_symbol_data.p_e_ratio = 15.1
        recommender = Recommender(self.mock_symbol_data)
        self.assertFalse(recommender.has_low_p_e_ratio())
