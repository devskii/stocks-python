import api
import time
import unittest


class TestApi(unittest.TestCase):
    def tearDown(self):
        time.sleep(1)
    
    def test_get_overview(self):
        symbol = "AAPL"
        data = api.get_stock_overview(symbol)
        self.assertEqual(data.get("Symbol"), symbol)

    def test_get_balance_sheet(self):
        symbol = "AAPL"
        data = api.get_stock_balance_sheet(symbol)
        self.assertEqual(data.get("symbol"), symbol)

    def test_get_earnings(self):
        symbol = "AAPL"
        data = api.get_stock_earnings(symbol)
        self.assertEqual(data.get("symbol"), symbol)

    def test_get_stock_quote(self):
        symbol = "AAPL"
        data = api.get_stock_quote(symbol)
        self.assertEqual(data["Global Quote"]["01. symbol"], symbol)

if __name__ == "__main__":
    unittest.main()
