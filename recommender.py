import api
import plotly.graph_objects as go
import pandas as pd
import sys
from pprint import pprint

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


def has_low_pe_ratio(earnings, quote):
    quarterly_earnings = earnings['quarterlyEarnings']
    recent_quarters_earnings = [float(quarter['reportedEPS']) for quarter in quarterly_earnings[:12]]
    average_annual_earnings = sum(recent_quarters_earnings) / 3
    price = float(quote['Global Quote']['05. price'])
    ratio = price / average_annual_earnings
    return ratio <= 15.0


def plot_dividends(time_series_monthly_adjusted):
    time_series_items = time_series_monthly_adjusted['Monthly Adjusted Time Series'].items()
    dividends = {date: float(info['7. dividend amount']) for date, info in time_series_items if float(info['7. dividend amount']) > 0 }
    df = pd.DataFrame(list(dividends.items()), columns=['Date', 'Dividend'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df.resample('M').asfreq()
    df.reset_index(inplace=True)
    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Dividend'], mode='markers'))
    fig.update_layout(title='Dividend History', xaxis_title='Date', yaxis_title='Dividend Amount')
    fig.show()


def analyze(symbol):
    overview = api.get_stock_overview(symbol)
    balance_sheet = api.get_stock_balance_sheet(symbol)
    earnings = api.get_stock_earnings(symbol)
    time_series_monthly_adjusted = api.get_stock_time_series_monthly_adjusted(symbol)
    quote = api.get_stock_quote(symbol)
    
    large = is_large_cap(overview)
    healthy_current = has_healthy_current_ratio(balance_sheet)
    earnings_consistent = has_consistent_earnings(earnings)
    earnings_growth = has_earnings_growth(earnings)
    low_pe = has_low_pe_ratio(earnings, quote)

    recommendation = large and healthy_current and earnings_consistent and earnings_growth and low_pe

    print("====== RECOMMENDATION ======")
    print(f"The recommendation for {symbol} is {recommendation}")
    print("Friendly reminder to check the dividend looks strong (increasing) and consistent (no gaps) for the past 20+ years.")
    print("--------- Criteria ---------")
    print(f"is_large_cap: {large}")
    print(f"has_healthy_current_ratio: {healthy_current}")
    print(f"has_consistent_earnings: {earnings_consistent}")
    print(f"has_earnings_growth: {earnings_growth}")
    print(f"has_low_pe_ratio: {low_pe}")
    plot_dividends(time_series_monthly_adjusted)
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
