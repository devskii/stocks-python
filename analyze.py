import os
import time
import plotly.graph_objects as go
import pandas as pd
import sys
from analysis_printer import AnalysisPrinter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from symbol_data import SymbolData


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
    else:
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
        fig.write_image("tmp/dividends.png")


def analyze(symbol):
    try:
        symbol_data = SymbolData(symbol)
    except KeyError:
        print(
            "We are exceeding the API rate limit. Please wait 60 seconds for it to reset. Sleeping..."
        )
        time.sleep(60)
        sys.exit(1)

    AnalysisPrinter(symbol_data).print_analysis()
    plot_dividends_as_tempfile(symbol_data.time_series_monthly_adjusted)


def print_analysis_to_tempfiles(symbol):
    old_stdout = sys.stdout
    sys.stdout = open("tmp/output.txt", "w")
    analyze(symbol)
    sys.stdout = old_stdout


def build_recommendation_pdf(symbol):
    doc = SimpleDocTemplate(f"reports/Recommendation for {symbol}.pdf", pagesize=letter)
    story = []
    with open("tmp/output.txt", "r") as f:
        styles = getSampleStyleSheet()
        for line in f:
            story.append(Paragraph(line, styles["Normal"]))
    if os.path.exists("tmp/dividends.png"):
        story.append(Image("tmp/dividends.png", width=400, height=300))
    story.append(PageBreak())
    doc.build(story)


def generate_report(symbol):
    print_analysis_to_tempfiles(symbol)
    build_recommendation_pdf(symbol)
    cleanup_temp_files()


def cleanup_temp_files():
    if os.path.exists("tmp/output.txt"):
        os.remove("tmp/output.txt")
    if os.path.exists("tmp/dividends.png"):
        os.remove("tmp/dividends.png")


def main():
    if len(sys.argv) > 1:
        comma_separated_symbols = sys.argv[1]
        symbols = comma_separated_symbols.split(",")
        for s in symbols:
            generate_report(s)
            print(
                f"Report generated for {s}, waiting 60 seconds before generating the next report to avoid API throttling..."
            )
            time.sleep(60)

    else:
        print("Please provide a ticker symbol as a command-line argument.")
        sys.exit(1)


if __name__ == "__main__":
    main()
