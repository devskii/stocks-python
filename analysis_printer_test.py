import unittest
from io import StringIO
from unittest.mock import Mock, patch

from analysis_printer import AnalysisPrinter
from symbol_data import SymbolData

SYMBOL = "FOO"
OVERVIEW = {"MarketCapitalization": 30000000001}
BALANCE_SHEET = {
    "quarterlyReports": [{"totalCurrentAssets": 2000, "totalCurrentLiabilities": 1000}]
}
EARNINGS = {
    "annualEarnings": [{"reportedEPS": 1.33}] * 3 + [{"reportedEPS": 1.0}] * 7,
    "quarterlyEarnings": [{"reportedEPS": 1.0}] * 12,
}
QUOTE = {
    "Global Quote": {"05. price": "60.00"},
}
FOO_SYMBOL_DATA = SymbolData(
    SYMBOL,
    OVERVIEW,
    BALANCE_SHEET,
    EARNINGS,
    QUOTE,
    time_series_monthly_adjusted=None,
)


class TestAnalyze(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_buy_recommendation(self, mock_stdout):
        printer = AnalysisPrinter(FOO_SYMBOL_DATA)
        printer.recommender.recommendation = Mock(return_value=True)
        expected_message = """====== RECOMMENDATION ======
The recommendation for FOO is True
"""
        printer.print_recommendation()
        self.assertEqual(expected_message, mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_sell_recommendation(self, mock_stdout):
        printer = AnalysisPrinter(FOO_SYMBOL_DATA)
        printer.recommender.recommendation = Mock(return_value=False)
        expected_message = """====== RECOMMENDATION ======
The recommendation for FOO is False
"""
        printer.print_recommendation()
        self.assertEqual(expected_message, mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_sell_recommendation(self, mock_stdout):
        printer = AnalysisPrinter(FOO_SYMBOL_DATA)
        printer.recommender.recommendation = Mock(return_value=False)
        expected_message = """====== RECOMMENDATION ======
The recommendation for FOO is False
"""
        printer.print_recommendation()
        self.assertEqual(expected_message, mock_stdout.getvalue())
