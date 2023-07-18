from symbol_data import SymbolData


SYMBOL = "FOO"
OVERVIEW = {"MarketCapitalization": 30000000001}
BALANCE_SHEET = {
    "quarterlyReports": [{"totalCurrentAssets": 2000, "totalCurrentLiabilities": 1000}]
}
EARNINGS = {
    "annualEarnings": [{"reportedEPS": 1.33}] * 3 + [{"reportedEPS": 1.0}] * 7,
    "quarterlyEarnings": [{"reportedEPS": 1.0}] * 12,
}
QUOTE = {
    "Global Quote": {"05. price": "60.00"},
}
FOO_SYMBOL_DATA = SymbolData(
    SYMBOL,
    OVERVIEW,
    BALANCE_SHEET,
    EARNINGS,
    QUOTE,
    time_series_monthly_adjusted=None,
)
