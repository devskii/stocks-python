import api


def is_large_cap(overview):
    mcap = int(overview["MarketCapitalization"])
    # print(format(mcap, ","))
    return mcap > 30000000000


def has_healthy_current_ratio(balance_sheet):
    quarterly_reports = balance_sheet["quarterlyReports"]
    totalCurrentAssets = int(quarterly_reports[0]["totalCurrentAssets"])
    totalCurrentLiabilities = int(quarterly_reports[0]["totalCurrentLiabilities"])

    currentRatio = totalCurrentAssets / totalCurrentLiabilities
    return currentRatio >= 1.5 and currentRatio <= 3


def analyze_example():
    symbol = "AAPL"

    overview = api.get_stock_overview(symbol)
    balance_sheet = api.get_stock_balance_sheet(symbol)

    size = is_large_cap(overview)
    current = has_healthy_current_ratio(balance_sheet)

    recommendation = size and current
    print(f"The recommendation for {symbol} is {recommendation}")
    print(f"is_large_cap: {size}")
    print(f"has_healthy_current_ratio: {current}")


def main():
    analyze_example()


if __name__ == "__main__":
    main()
