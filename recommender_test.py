import recommender
import sys
import unittest
from unittest.mock import patch
from io import StringIO


class TestGetStockData(unittest.TestCase):
    def test_extract_market_cap(self):
        market_cap = 30000000001
        overview = {"MarketCapitalization": market_cap}
        self.assertEqual(recommender.extract_market_cap(overview), market_cap)

    def test_large_cap(self):
        market_cap = 30000000001
        self.assertTrue(recommender.is_large_cap(market_cap))

    def test_not_large_cap(self):
        market_cap = 29999999999
        self.assertFalse(recommender.is_large_cap(market_cap))

    def test_extract_current_ratio(self):
        balance_sheet = {
            "quarterlyReports": [
                {"totalCurrentAssets": 2000, "totalCurrentLiabilities": 1000}
            ]
        }
        self.assertEqual(2.0, recommender.extract_current_ratio(balance_sheet))

    def test_has_healthy_current_ratio(self):
        current_ratio = 2.0
        self.assertTrue(recommender.has_healthy_current_ratio(current_ratio))

    def test_has_unhealthy_high_current_ratio(self):
        current_ratio = 3.001
        self.assertFalse(recommender.has_healthy_current_ratio(current_ratio))

    def test_has_unhealthy_low_current_ratio(self):
        current_ratio = 1.499
        self.assertFalse(recommender.has_healthy_current_ratio(current_ratio))

    def test_extract_decade_of_annual_earnings(self):
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
                {"reportedEPS": 0.1},
            ]
        }
        self.assertEqual(
            [0.1] * 10, recommender.extract_decade_of_annual_earnings(earnings)
        )

    def test_has_consistent_earnings(self):
        decade_of_annual_earnings = [0.1] * 10
        self.assertTrue(recommender.has_consistent_earnings(decade_of_annual_earnings))

    def test_has_inconsistent_earnings(self):
        decade_of_annual_earnings = [-0.1] + [0.1] * 9
        self.assertFalse(recommender.has_consistent_earnings(decade_of_annual_earnings))

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
                {"reportedEPS": 1.0},
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
                {"reportedEPS": 1.0},
            ]
        }
        self.assertFalse(recommender.has_earnings_growth(earnings))

    def test_has_low_pe_ratio(self):
        earnings = {
            "quarterlyEarnings": [
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
            ]
        }
        quote = {
            "Global Quote": {"05. price": "60.00"},
        }
        self.assertTrue(recommender.has_low_pe_ratio(earnings, quote))

    def test_has_high_pe_ratio(self):
        earnings = {
            "quarterlyEarnings": [
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
                {"reportedEPS": 1.0},
            ]
        }
        quote = {"Global Quote": {"05. price": "60.01"}}
        self.assertFalse(recommender.has_low_pe_ratio(earnings, quote))

    @patch.object(sys, "argv", ["recommender.py"])
    def test_no_ticker_symbol(self):
        # Create a new StringIO object and redirect stdout to it
        captured_output = StringIO()
        sys.stdout = captured_output

        with self.assertRaises(SystemExit):
            recommender.main()

        # Reset stdout to its normal value
        sys.stdout = sys.__stdout__

        # Check the value that was printed
        self.assertEqual(
            captured_output.getvalue().strip(),
            "Please provide a ticker symbol as a command-line argument.",
        )


if __name__ == "__main__":
    unittest.main()
