import stocks
import unittest


class TestGetStockData(unittest.TestCase):
    def test_large_cap(self):
        overview = {"MarketCapitalization": 30000000001}
        self.assertTrue(stocks.is_large_cap(overview))

    def test_not_large_cap(self):
        overview = {"MarketCapitalization": 29999999999}
        self.assertFalse(stocks.is_large_cap(overview))

    def test_has_healthy_current_ratio(self):
        balance_sheet = {
            "quarterlyReports": [{
                "totalCurrentAssets": 2000,
                "totalCurrentLiabilities": 1000
            }]
        }
        self.assertTrue(stocks.has_healthy_current_ratio(balance_sheet))

    def test_has_unhealthy_high_current_ratio(self):
        balance_sheet = {
            "quarterlyReports": [{
                "totalCurrentAssets": 3001,
                "totalCurrentLiabilities": 1000
            }]
        }
        self.assertFalse(stocks.has_healthy_current_ratio(balance_sheet))

    def test_has_unhealthy_low_current_ratio(self):
        balance_sheet = {
            "quarterlyReports": [{
                "totalCurrentAssets": 1499,
                "totalCurrentLiabilities": 1000
            }]
        }
        self.assertFalse(stocks.has_healthy_current_ratio(balance_sheet))


if __name__ == "__main__":
    unittest.main()
