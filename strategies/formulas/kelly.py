import os
import pandas as pd
import numpy as np
import json
import finnhub
from datetime import datetime, timedelta
from dotenv import load_dotenv

risk_free_rate = 0.013 


load_dotenv()


finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
base_dir = "../data"
scores = {}
kelly_fractions = {}

risk_free_rate = 0.013  # Update this value with actual data

def calculate_score(data, window, risk_free_rate):
    data_last30 = data[-window:].copy()
    data_last30['PctChange'] = data_last30.pct_change()
    volatility_last30 = data_last30['PctChange'].std() * np.sqrt(252)
    mean_return = data_last30['PctChange'].mean() * 252
    sharpe_ratio = (mean_return - risk_free_rate) / volatility_last30
    return sharpe_ratio

def calculate_kelly_fraction(data, window, risk_free_rate):
    data_last30 = data[-window:].copy()
    data_last30['PctChange'] = data_last30.pct_change()
    volatility_last30 = data_last30['PctChange'].std() * np.sqrt(252)
    mean_return = data_last30['PctChange'].mean() * 252
    excess_return = mean_return - risk_free_rate
    kelly_fraction = excess_return / (volatility_last30 ** 2)
    return kelly_fraction

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
        df['MA14'] = df['Close'].rolling(window=14).mean()
        ma14_last = df['MA14'].iloc[-1]
        ma14_prev = df['MA14'].iloc[-2]
        if ma14_last > ma14_prev:
            score = calculate_score(df['Close'], 30, risk_free_rate)
            scores[ticker] = score
            kelly_fraction = calculate_kelly_fraction(df['Close'], 30, risk_free_rate)
            kelly_fractions[ticker] = kelly_fraction

# Normalize the Kelly fractions so they add up to 1
total_kelly_fraction = sum(kelly_fractions.values())
kelly_fractions = {ticker: frac/total_kelly_fraction for ticker, frac in kelly_fractions.items()}

num_tickers = 15
top = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:num_tickers]
top_tickers = [item[0] for item in top]

print(f"Selected stocks: {top_tickers}")

budget = 10000

# Allocate funds according to Kelly fractions
funds = {stock: kelly_fractions[stock] * budget for stock in top_tickers}

dataframes = []
for ticker in top_tickers:
    ticker_dir = os.path.join(base_dir, ticker)
    df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
    df["Ticker"] = ticker
    dataframes.append(df)

all_data = pd.concat(dataframes)
shares = {stock: funds[stock] / all_data[(all_data["Ticker"] == stock)].iloc[0]["Close"] for stock in top_tickers}

portfolio_value = sum([shares[stock] * all_data[(all_data["Ticker"]
                      == stock)].iloc[-1]["Close"] for stock in top_tickers])

earned = portfolio_value/(budget/100.0)
print(
    f"Final value using this strategy: ${portfolio_value}, which is a %{earned:.2f} return")

json_file_path = 'output.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)

if "iman" in data["Shares"]:
    data["Shares"]["iman"].update(shares)
else:
    data["Shares"]["iman"] = shares

data["iman"] = earned

for strategy in data["Shares"]:
    data["Shares"][strategy] = {k: v for k, v in sorted(data["Shares"][strategy].items(), key=lambda item: item[1])}

with open(json_file_path, 'w') as file:
    json.dump(data, file)