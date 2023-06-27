import requests


def get_stock_overview(symbol, api_key):
    base_url = "https://www.alphavantage.co/query?"
    function = "OVERVIEW"
    datatype = "json"

    request_url = f"{base_url}function={function}&symbol={symbol}&apikey={api_key}&datatype={datatype}"

    response = requests.get(request_url)
    data = response.json()
    return data


def get_stock_balance_sheet(symbol, api_key):
    base_url = "https://www.alphavantage.co/query?"
    function = "BALANCE_SHEET"
    datatype = "json"

    request_url = f"{base_url}function={function}&symbol={symbol}&apikey={api_key}&datatype={datatype}"

    response = requests.get(request_url)
    data = response.json()
    return data


def analyze_stock_overview(overview, balance_sheet):
    quarterly_reports = balance_sheet["quarterlyReports"]
    totalCurrentAssets = int(quarterly_reports[0]["totalCurrentAssets"])
    totalCurrentLiabilities = int(quarterly_reports[0]["totalCurrentLiabilities"])

    currentRatio = totalCurrentAssets / totalCurrentLiabilities
    print(totalCurrentAssets)
    print(totalCurrentLiabilities)
    print(currentRatio)

    mcap = int(overview["MarketCapitalization"])
    # print(format(mcap, ","))
    if mcap > 30000000000:
        return "buy"
    else:
        return "sell"


def analyze_example():
    symbol = "AAPL"
    api_key = "***REMOVED***"

    overview = get_stock_overview(symbol, api_key)
    balance_sheet = get_stock_balance_sheet(symbol, api_key)

    recommendation = analyze_stock_overview(overview, balance_sheet)
    print(f"The recommendation for {symbol} is {recommendation}")


def main():
    analyze_example()


if __name__ == "__main__":
    main()
