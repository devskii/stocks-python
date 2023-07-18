import unittest
from io import StringIO
from unittest.mock import Mock, patch

from analysis_printer import AnalysisPrinter
from foo_symbol_data import FOO_SYMBOL_DATA


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
