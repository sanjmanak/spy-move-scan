# spy-move-scan
A Python-based tool (optimized for Google Colab) that helps traders identify the last time SPY moved a configurable number of points within a given time window. Ideal for spotting volatility surges, backtesting entry strategies, and timing trade setups based on recent price action

# 📈 Weekly Highs and Lows by Day of Week (SPY Analysis)

This Python script analyzes SPY (S&P 500 ETF) historical data over the past 5 years to uncover patterns in which **day of the week** most often sees **weekly highs and lows**.

---

## 🔍 What It Does

- Fetches 5 years of SPY price data using `yfinance`
- Resamples it to weekly intervals
- Identifies the **weekday** when the high and low of each week occurred
- Calculates:
  - 📅 Last 10 dates for each weekday's highs and lows
  - ⏳ Days since the last high or low per weekday
  - 🔁 Average number of days between highs/lows per weekday
  - 🔢 Total count of highs and lows per weekday
- Outputs:
  - ✅ Neatly formatted summary tables in the console (via `tabulate`)
  - 📊 Grouped bar chart (via Plotly) for visual comparison

---

## 📦 Requirements

Make sure you have the following Python packages installed:

```bash
pip install yfinance pandas plotly tabulate

