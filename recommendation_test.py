import unittest
from unittest.mock import MagicMock

from recommender import Recommender


class TestRecommendation(unittest.TestCase):
    BUY = "BUY"
    SELL = "SELL"

    def setUp(self):
        self.recommender = Recommender(symbol_data=None)
        self.recommender.is_large_cap = MagicMock(return_value=True)
        self.recommender.has_healthy_current_ratio = MagicMock(return_value=True)
        self.recommender.has_consistent_earnings = MagicMock(return_value=True)
        self.recommender.has_earnings_growth = MagicMock(return_value=True)
        self.recommender.has_low_p_e_ratio = MagicMock(return_value=True)

    def test_buy(self):
        self.assertTrue(self.recommender.recommendation())

    def test_sell_not_large(self):
        self.recommender.is_large_cap = MagicMock(return_value=False)
        self.assertFalse(self.recommender.recommendation())

    def test_sell_unhealthy_current_ratio(self):
        self.recommender.has_healthy_current_ratio = MagicMock(return_value=False)
        self.assertFalse(self.recommender.recommendation())

    def test_sell_inconsistent_earnings(self):
        self.recommender.has_consistent_earnings = MagicMock(return_value=False)
        self.assertFalse(self.recommender.recommendation())

    def test_sell_insufficient_earnings_growth(self):
        self.recommender.has_earnings_growth = MagicMock(return_value=False)
        self.assertFalse(self.recommender.recommendation())

    def test_sell_high_p_e_ratio(self):
        self.recommender.has_low_p_e_ratio = MagicMock(return_value=False)
        self.assertFalse(self.recommender.recommendation())
