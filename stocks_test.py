import stocks
import unittest


class TestGetStockData(unittest.TestCase):
    def test_get_overview(self):
        symbol = "AAPL"
        api_key = "***REMOVED***"
        data = stocks.get_stock_overview(symbol, api_key)
        self.assertEqual(data.get("Symbol"), symbol)

    def test_get_balance_sheet(self):
        symbol = "AAPL"
        api_key = "***REMOVED***"
        data = stocks.get_stock_balance_sheet(symbol, api_key)
        self.assertEqual(data.get("Symbol"), symbol)

    def test_buy_large(self):
        data = {"MarketCapitalization": 30000000001}
        self.assertEqual("buy", stocks.analyze_stock_overview(data))

    def test_sell_small(self):
        data = {"MarketCapitalization": 29999999999}
        self.assertEqual("sell", stocks.analyze_stock_overview(data))


if __name__ == "__main__":
    unittest.main()
