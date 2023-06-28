import requests


def get_stock_overview(symbol):
    return get_function(symbol, "OVERVIEW")


def get_stock_balance_sheet(symbol):
    return get_function(symbol, "BALANCE_SHEET")


def get_stock_earnings(symbol):
    return get_function(symbol, "EARNINGS")


def get_stock_time_series_monthly_adjusted(symbol):
    return get_function(symbol, "TIME_SERIES_MONTHLY_ADJUSTED")


def get_stock_quote(symbol):
    return get_function(symbol, "GLOBAL_QUOTE")


def get_function(symbol, function):
    api_key = "***REMOVED***"
    base_url = "https://www.alphavantage.co/query?"
    datatype = "json"

    request_url = f"{base_url}function={function}&symbol={symbol}&apikey={api_key}&datatype={datatype}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"API request failed with status code {response.status_code}")
        print(response.text)
