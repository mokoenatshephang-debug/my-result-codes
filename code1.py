# Install/upgrade yfinance
#!pip install -q yfinance --upgrade

import yfinance as yf
import matplotlib.pyplot as plt

# Define tickers and benchmark
tickers = ['XLE','BZ', 'NG', 'BNO',
    'NEE', 'BEP', 'FSLR', 'GEV',
    'CWEN', 'RNW',
    'EFT', 'CLNE', 'EQT', 'SM',
    'CRGY', 'NGS']  # Portfolio assets
benchmark_ticker = '^GSPC'  # S&P 500 as benchmark
start_date = '2010-01-01'
end_date = '2026-11-20'

# Download data for tickers
# data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
data = yf.download(
    tickers,
    start=start_date,
    end=end_date,
    auto_adjust=True
)['Close']
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Define tickers
# -----------------------------
tickers = ['XLE',
    'BZ', 'NG', 'BNO',
    'NEE', 'BEP', 'FSLR', 'GEV',
    'CWEN', 'RNW',
    'EFT', 'CLNE', 'EQT', 'SM',
    'CRGY', 'NGS'
]

start_date = '2010-01-02'
end_date = '2026-11-20'

# -----------------------------
# Download data
# -----------------------------
data = yf.download(
    tickers,
    start=start_date,
    end=end_date,
    auto_adjust=False,
    group_by='column',
    progress=False
)

# -----------------------------
# Check available columns
# -----------------------------
print("Columns downloaded:")
print(data.columns)

# -----------------------------
# Extract Adjusted Close prices
# -----------------------------
if 'Adj Close' in data.columns.get_level_values(0):
    prices = data['Adj Close']
else:
    print("Adj Close not available. Using Close prices.")
    prices = data['Close']

# -----------------------------
# First available date per asset
# -----------------------------
print("\nFirst available observation date:")
for ticker in prices.columns:
    first_date = prices[ticker].dropna().index.min()
    print(f"{ticker}: {first_date.date()}")

# -----------------------------
# Determine common sample period
# -----------------------------
common_start = max(
    prices[ticker].dropna().index.min()
    for ticker in prices.columns
)

print("\nCommon sample starts on:", common_start.date())

# Keep only common sample
prices = prices.loc[common_start:]

# Remove assets with excessive missing values
prices = prices.dropna(axis=1, thresh=int(0.8*len(prices)))

# Forward-fill occasional gaps
prices = prices.ffill()

# Drop remaining missing observations
prices = prices.dropna()

# -----------------------------
# Compute log returns
# -----------------------------
log_returns = np.log(prices / prices.shift(1))
log_returns = log_returns.dropna()

print("\nLog returns shape:")
print(log_returns.shape)

# -----------------------------
# Descriptive statistics
# -----------------------------
summary = pd.DataFrame({
    'Mean': log_returns.mean(),
    'Std Dev': log_returns.std(),
    'Min': log_returns.min(),
    'Max': log_returns.max(),
    'Skewness': log_returns.skew(),
    'Kurtosis': log_returns.kurtosis()
})
