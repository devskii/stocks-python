import os
import sys
import time

import pandas as pd
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate

import api
from analysis_printer import AnalysisPrinter


def main():
    if len(sys.argv) > 1:
        comma_separated_symbols = sys.argv[1]
        symbols = comma_separated_symbols.split(",")
        generate_reports(symbols)
    else:
        print("Please provide a ticker symbol as a command-line argument.")
        sys.exit(1)


def generate_reports(symbols):
    for i in range(len(symbols)):
        symbol = symbols[i]
        generate_report(symbol)
        print(f"Report generated for {symbol}")
        if i != len(symbols) - 1:
            print(
                f"Waiting 60 seconds before generating the next report ({symbols[i+1]}) to avoid API throttling..."
            )
            time.sleep(60)


def generate_report(symbol):
    print_analysis_to_tempfiles(symbol)
    build_recommendation_pdf(symbol)
    cleanup_temp_files()


def print_analysis_to_tempfiles(symbol):
    old_stdout = sys.stdout
    sys.stdout = open("tmp/output.txt", "w")
    analyze(symbol)
    sys.stdout = old_stdout


def analyze(symbol):
    try:
        symbol_data = api.get_symbol_data(symbol)
    except KeyError:
        print("Exceeding API rate limit. Please wait 60s for it to reset...")
        time.sleep(60)
        sys.exit(1)

    AnalysisPrinter(symbol_data).print_analysis()
    plot_dividends_as_tempfile(symbol_data.time_series_monthly_adjusted)


def build_recommendation_pdf(symbol):
    doc = SimpleDocTemplate(f"reports/Recommendation for {symbol}.pdf", pagesize=letter)
    story = []
    with open("tmp/output.txt", "r") as file:
        styles = getSampleStyleSheet()
        for line in file:
            story.append(Paragraph(line, styles["Normal"]))
    if os.path.exists("tmp/dividends.png"):
        story.append(Image("tmp/dividends.png", width=400, height=300))
    story.append(PageBreak())
    doc.build(story)


def plot_dividends_as_tempfile(time_series_monthly_adjusted):
    time_series_items = time_series_monthly_adjusted[
        "Monthly Adjusted Time Series"
    ].items()
    dividends = {
        date: float(info["7. dividend amount"])
        for date, info in time_series_items
        if float(info["7. dividend amount"]) > 0
    }
    if len(dividends) == 0:
        print("No dividend history.")
        return

    data_frame = pd.DataFrame(list(dividends.items()), columns=["Date", "Dividend"])
    data_frame["Date"] = pd.to_datetime(data_frame["Date"])
    data_frame.set_index("Date", inplace=True)
    data_frame = data_frame.resample("M").asfreq()
    data_frame.reset_index(inplace=True)
    fig = go.Figure(
        data=go.Scatter(x=data_frame["Date"], y=data_frame["Dividend"], mode="markers")
    )
    fig.update_layout(
        title="Dividend History<br><sub>Friendly reminder: check for strong (increasing) and consistent (no gaps) for 20+ years.</sub>",
        xaxis_title="Date",
        yaxis_title="Dividend Amount",
    )
    fig.write_image("tmp/dividends.png")


def cleanup_temp_files():
    if os.path.exists("tmp/output.txt"):
        os.remove("tmp/output.txt")
    if os.path.exists("tmp/dividends.png"):
        os.remove("tmp/dividends.png")


if __name__ == "__main__":
    main()
