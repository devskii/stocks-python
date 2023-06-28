import recommender
import unittest


class TestGetStockData(unittest.TestCase):
    def test_large_cap(self):
        overview = {"MarketCapitalization": 30000000001}
        self.assertTrue(recommender.is_large_cap(overview))

    def test_not_large_cap(self):
        overview = {"MarketCapitalization": 29999999999}
        self.assertFalse(recommender.is_large_cap(overview))

    def test_has_healthy_current_ratio(self):
        balance_sheet = {
            "quarterlyReports": [{
                "totalCurrentAssets": 2000,
                "totalCurrentLiabilities": 1000
            }]
        }
        self.assertTrue(recommender.has_healthy_current_ratio(balance_sheet))

    def test_has_unhealthy_high_current_ratio(self):
        balance_sheet = {
            "quarterlyReports": [{
                "totalCurrentAssets": 3001,
                "totalCurrentLiabilities": 1000
            }]
        }
        self.assertFalse(recommender.has_healthy_current_ratio(balance_sheet))

    def test_has_unhealthy_low_current_ratio(self):
        balance_sheet = {
            "quarterlyReports": [{
                "totalCurrentAssets": 1499,
                "totalCurrentLiabilities": 1000
            }]
        }
        self.assertFalse(recommender.has_healthy_current_ratio(balance_sheet))

    def test_has_consistent_earnings(self):
        earnings = {
            "annualEarnings": [
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1}
            ]
        }
        self.assertTrue(recommender.has_consistent_earnings(earnings))

    def test_has_inconsistent_earnings(self):
        earnings = {
            "annualEarnings": [
                {"reportedEPS": -0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1},
                {"reportedEPS": 0.1}
            ]
        }
        self.assertFalse(recommender.has_consistent_earnings(earnings))

    def test_has_earnings_growth(self):
        earnings = {
            "annualEarnings": [
                {"reportedEPS": 1.33},
                {"reportedEPS": 1.33},
                {"reportedEPS": 1.33},
                {"reportedEPS": 0},
                {"reportedEPS": 0},
                {"reportedEPS": 0},
                {"reportedEPS": 0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0}
            ]
        }
        self.assertTrue(recommender.has_earnings_growth(earnings))

    def test_has_insufficient_earnings_growth(self):
        earnings = {
            "annualEarnings": [
                {"reportedEPS": 1.32},
                {"reportedEPS": 1.32},
                {"reportedEPS": 1.32},
                {"reportedEPS": 0},
                {"reportedEPS": 0},
                {"reportedEPS": 0},
                {"reportedEPS": 0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0}
            ]
        }
        self.assertFalse(recommender.has_earnings_growth(earnings))

if __name__ == "__main__":
    unittest.main()
