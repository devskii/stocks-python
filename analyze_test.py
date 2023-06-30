import analyze
import sys
import unittest
from io import StringIO
from unittest.mock import patch


class TestAnalyze(unittest.TestCase):
    @patch.object(sys, "argv", ["recommender.py"])
    def test_no_ticker_symbol(self):
        # Create a new StringIO object and redirect stdout to it
        captured_output = StringIO()
        sys.stdout = captured_output

        with self.assertRaises(SystemExit):
            analyze.main()

        # Reset stdout to its normal value
        sys.stdout = sys.__stdout__

        # Check the value that was printed
        self.assertEqual(
            captured_output.getvalue().strip(),
            "Please provide a ticker symbol as a command-line argument.",
        )


if __name__ == "__main__":
    unittest.main()
