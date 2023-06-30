import time
import plotly.graph_objects as go
import pandas as pd
import sys
from recommender import Recommender
from symbol_data import SymbolData


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
        title="Dividend History<br><sub>Friendly reminder to check the dividend looks strong (increasing) and consistent (no gaps) for the past 20+ years.</sub>",
        xaxis_title="Date",
        yaxis_title="Dividend Amount",
    )
    fig.show()


def bold(message):
    return f"\033[1m{message}\033[0m"


def analyze(symbol):
    try:
        symbol_data = SymbolData(symbol)
    except KeyError:
        print(
            "We are exceeding the API rate limit. Please wait 60 seconds for it to reset. Sleeping..."
        )
        time.sleep(60)
        sys.exit(1)

    recommender = Recommender(symbol_data)

    print(bold("====== RECOMMENDATION ======"))
    print(f"The recommendation for {symbol} is {recommender.recommendation()}")
    print(bold("--------- Criteria ---------"))
    print(f"is_large_cap: {recommender.is_large_cap()}")
    print(f"has_healthy_current_ratio: {recommender.has_healthy_current_ratio()}")
    print(f"has_consistent_earnings: {recommender.has_consistent_earnings()}")
    print(f"has_earnings_growth: {recommender.has_earnings_growth()}")
    print(f"has_low_pe_ratio: {recommender.has_low_p_e_ratio()}")
    plot_dividends(symbol_data.time_series_monthly_adjusted)
    print(bold("--------- Details ----------"))
    print(f"Market Cap: {format(symbol_data.market_cap, ',')}")
    print(f"Current Ratio: {round(symbol_data.current_ratio, 2)}")
    print(f"10 years of Annual EPS: {symbol_data.decade_of_annual_earnings}")
    print(
        f"Earnings Growth over last decade: {round(symbol_data.earnings_growth_past_decade * 100, 0)}%"
    )
    print(
        f"P/E Ratio based on most recent 12 quarters: {round(symbol_data.p_e_ratio, 2)}"
    )
    print(bold("============================"))


def main():
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
        analyze(symbol)
    else:
        print("Please provide a ticker symbol as a command-line argument.")
        sys.exit(1)


if __name__ == "__main__":
    main()
