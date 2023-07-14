import os
import pandas as pd
import numpy as np
import json

base_dir = "../data"
scores = {}

def calculate_score(data, window):
    data_last30 = data[-window:].copy()
    data_last30['PctChange'] = data_last30.pct_change()
    volatility_last30 = data_last30['PctChange'].std() * (365 ** 0.5)
    score = 1 / volatility_last30
    return score



for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
        df['MA14'] = df['Close'].rolling(window=14).mean()
        ma14_last = df['MA14'].iloc[-1]
        ma14_prev = df['MA14'].iloc[-2]
        if ma14_last > ma14_prev:
            score = calculate_score(df['Close'], 30)
            scores[ticker] = score

num_tickers = 10
top = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:num_tickers]
top_tickers = [item[0] for item in top]

print(f"Selected stocks: {top_tickers}")

budget = 10000
funds = {stock: budget / len(top_tickers) for stock in top_tickers}

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

output = ['iman',earned]
