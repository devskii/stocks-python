import time
import api
import plotly.graph_objects as go
import pandas as pd
import sys


def is_large_cap(market_cap):
    return market_cap > 30000000000


def has_healthy_current_ratio(current_ratio):
    return current_ratio >= 1.5 and current_ratio <= 3


def has_consistent_earnings(decade_of_annual_earnings):
    return all(eps >= 0 for eps in decade_of_annual_earnings)


def has_earnings_growth(earnings_growth_past_decade):
    return earnings_growth_past_decade >= 0.33


def has_low_p_e_ratio(p_e_ratio):
    return p_e_ratio <= 15.0


def plot_dividends(time_series_monthly_adjusted):
    time_series_items = time_series_monthly_adjusted[
        "Monthly Adjusted Time Series"
    ].items()
    dividends = {
        date: float(info["7. dividend amount"])
        for date, info in time_series_items
        if float(info["7. dividend amount"]) > 0
    }
    df = pd.DataFrame(list(dividends.items()), columns=["Date", "Dividend"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df = df.resample("M").asfreq()
    df.reset_index(inplace=True)
    fig = go.Figure(data=go.Scatter(x=df["Date"], y=df["Dividend"], mode="markers"))
    fig.update_layout(
        title="Dividend History", xaxis_title="Date", yaxis_title="Dividend Amount"
    )
    fig.show()


def extract_market_cap(overview):
    return int(overview["MarketCapitalization"])


def extract_current_ratio(balance_sheet):
    quarterly_reports = balance_sheet["quarterlyReports"]
    total_current_assets = int(quarterly_reports[0]["totalCurrentAssets"])
    total_current_liabilities = int(quarterly_reports[0]["totalCurrentLiabilities"])
    return total_current_assets / total_current_liabilities


def extract_decade_of_annual_earnings(earnings):
    return [float(year["reportedEPS"]) for year in earnings["annualEarnings"][:10]]


def compute_earnings_growth_past_decade(decade_of_annual_earnings):
    most_recent_three_years = sum(decade_of_annual_earnings[:3])
    decade_beginning_three_years = sum(decade_of_annual_earnings[7:10])
    difference = most_recent_three_years - decade_beginning_three_years
    growth = difference / decade_beginning_three_years
    return growth


def extract_p_e_ratio(earnings, quote):
    quarterly_earnings = earnings["quarterlyEarnings"]
    recent_quarters_earnings = [
        float(quarter["reportedEPS"]) for quarter in quarterly_earnings[:12]
    ]
    average_annual_earnings = sum(recent_quarters_earnings) / 3
    price = float(quote["Global Quote"]["05. price"])
    return price / average_annual_earnings


def analyze(symbol):
    overview = api.get_stock_overview(symbol)
    balance_sheet = api.get_stock_balance_sheet(symbol)
    earnings = api.get_stock_earnings(symbol)
    time_series_monthly_adjusted = api.get_stock_time_series_monthly_adjusted(symbol)
    quote = api.get_stock_quote(symbol)

    try:
        market_cap = extract_market_cap(overview)
        current_ratio = extract_current_ratio(balance_sheet)
        decade_of_annual_earnings = extract_decade_of_annual_earnings(earnings)
        earnings_growth_past_decade = compute_earnings_growth_past_decade(
            decade_of_annual_earnings
        )
        p_e_ratio = extract_p_e_ratio(earnings, quote)
    except KeyError:
        print(
            "We are exceeding the API rate limit. Please wait 60 seconds for it to reset. Sleeping..."
        )
        time.sleep(60)
        sys.exit(1)

    large = is_large_cap(market_cap)
    healthy_current = has_healthy_current_ratio(current_ratio)
    earnings_consistent = has_consistent_earnings(decade_of_annual_earnings)
    earnings_growth = has_earnings_growth(earnings_growth_past_decade)
    low_pe = has_low_p_e_ratio(p_e_ratio)

    recommendation = (
        large and healthy_current and earnings_consistent and earnings_growth and low_pe
    )

    print("====== RECOMMENDATION ======")
    print(f"The recommendation for {symbol} is {recommendation}")
    print(
        "Friendly reminder to check the dividend looks strong (increasing) and consistent (no gaps) for the past 20+ years."
    )
    print("--------- Criteria ---------")
    print(f"is_large_cap: {large}")
    print(f"has_healthy_current_ratio: {healthy_current}")
    print(f"has_consistent_earnings: {earnings_consistent}")
    print(f"has_earnings_growth: {earnings_growth}")
    print(f"has_low_pe_ratio: {low_pe}")
    plot_dividends(time_series_monthly_adjusted)
    print("--------- Details ----------")
    print(f"Market Cap: {format(market_cap, ',')}")
    print(f"Current Ratio: {round(current_ratio, 2)}")
    print(f"10 years of Annual EPS: {decade_of_annual_earnings}")
    print(
        f"Earnings Growth over last decade: {round(earnings_growth_past_decade * 100, 0)}%"
    )
    print(f"P/E Ratio based on most recent 12 quarters: {round(p_e_ratio, 2)}")
    print("============================")


def main():
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
        analyze(symbol)
    else:
        print("Please provide a ticker symbol as a command-line argument.")
        sys.exit(1)


if __name__ == "__main__":
    main()
