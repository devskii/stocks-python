import time
import plotly.graph_objects as go
import pandas as pd
import sys

from symbol_data import SymbolData


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


def analyze(symbol):
    try:
        symbol_data = SymbolData(symbol)
    except KeyError:
        print(
            "We are exceeding the API rate limit. Please wait 60 seconds for it to reset. Sleeping..."
        )
        time.sleep(60)
        sys.exit(1)

    large = is_large_cap(symbol_data.market_cap)
    healthy_current = has_healthy_current_ratio(symbol_data.current_ratio)
    earnings_consistent = has_consistent_earnings(symbol_data.decade_of_annual_earnings)
    earnings_growth = has_earnings_growth(symbol_data.earnings_growth_past_decade)
    low_pe = has_low_p_e_ratio(symbol_data.p_e_ratio)

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
    plot_dividends(symbol_data.time_series_monthly_adjusted)
    print("--------- Details ----------")
    print(f"Market Cap: {format(symbol_data.market_cap, ',')}")
    print(f"Current Ratio: {round(symbol_data.current_ratio, 2)}")
    print(f"10 years of Annual EPS: {symbol_data.decade_of_annual_earnings}")
    print(
        f"Earnings Growth over last decade: {round(symbol_data.earnings_growth_past_decade * 100, 0)}%"
    )
    print(
        f"P/E Ratio based on most recent 12 quarters: {round(symbol_data.p_e_ratio, 2)}"
    )
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
