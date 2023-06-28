import api


def is_large_cap(overview):
    mcap = int(overview["MarketCapitalization"])
    # print(format(mcap, ","))
    return mcap > 30000000000


def has_healthy_current_ratio(balance_sheet):
    quarterly_reports = balance_sheet["quarterlyReports"]
    total_current_assets = int(quarterly_reports[0]["totalCurrentAssets"])
    total_current_liabilities = int(quarterly_reports[0]["totalCurrentLiabilities"])
    current_ratio = total_current_assets / total_current_liabilities
    return current_ratio >= 1.5 and current_ratio <= 3


def has_consistent_earnings(earnings):
    annual_earnings = earnings['annualEarnings']
    return all(float(year["reportedEPS"]) >= 0 for year in annual_earnings)


def has_earnings_growth(earnings):
    annual_reported_eps = [float(year['reportedEPS']) for year in earnings['annualEarnings']]
    most_recent_three_years = sum(annual_reported_eps[:3])
    decade_beginning_three_years = sum(annual_reported_eps[7:10])
    difference = most_recent_three_years - decade_beginning_three_years
    growth = difference / decade_beginning_three_years
    return growth >= 0.33


def analyze_example():
    symbol = "AAPL"

    overview = api.get_stock_overview(symbol)
    balance_sheet = api.get_stock_balance_sheet(symbol)
    earnings = api.get_stock_earnings(symbol)

    size = is_large_cap(overview)
    current = has_healthy_current_ratio(balance_sheet)
    earnings_consistent = has_consistent_earnings(earnings)
    earnings_growth = has_earnings_growth(earnings)

    recommendation = size and current and earnings_consistent and earnings_growth

    print("====== RECOMMENDATION ======")
    print(f"The recommendation for {symbol} is {recommendation}")
    print("--------- Criteria ---------")
    print(f"is_large_cap: {size}")
    print(f"has_healthy_current_ratio: {current}")
    print(f"has_consistent_earnings: {earnings_consistent}")
    print(f"has_earnings_growth: {earnings_growth}")
    print("============================")

def main():
    analyze_example()


if __name__ == "__main__":
    main()
