# Intro
This is an application that tells you whether or not to buy a stock, based on a set of criteria from the book "The Intelligent Investor" by Warren Buffett's mentor, Benjamin Graham, one of the most successful investors of the 20th century.

# Instructions
1. In `watch_list.txt`, add a comma-separated list of stock tickers you'd like to analyze. For example, `AAPL,TSLA`.
1. Run `pip3 install -r requirements.txt`
1. Run `python3 analyze.py $(cat watch_list.txt)`
1. Wait for the script to finish.
1. Open the PDFs in the reports/ directory to see the recommendations.

# Checks
## Running unit tests
See the file, `.github/workflows/unittest.yml`

## Running linter
See the file, `.github/workflows/pylint.yml`

# API docs
https://www.alphavantage.co/documentation/
https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo