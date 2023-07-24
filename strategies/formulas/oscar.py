import os
import pandas as pd
import numpy as np
import json
import yfinance as yf

base_dir = "../data"
totals = {}

def calculate_score(data):
    low_min = data['Low'].rolling(window=14).min()
    high_max = data['High'].rolling(window=14).max()

    data['%K'] = 100*((data['Close'] - low_min) / (high_max - low_min))

    data['%D'] = data['%K'].rolling(window=3).mean()
    
    data['BuySignal'] = (data['%K'] < 20) & (data['%D'] < 20)
    buy_signals = data[data['BuySignal']].shape[0]
    return buy_signals

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
        
        if 'High' not in df.columns or 'Low' not in df.columns:
            ticker_data = yf.download(ticker, start=df['Date'].min(), end=df['Date'].max())
            df['High'] = ticker_data['High']
            df['Low'] = ticker_data['Low']
        
        buy_signals = calculate_score(df)
        totals[ticker] = buy_signals

num_tickers = 6
top = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:num_tickers]
top_tickers = [item[0] for item in top]

print(f"Selected stocks: {top_tickers}")

budget = 10000
funds_ratios = [0.38, 0.26, 0.12, 0.08, 0.08, 0.08]
funds = {stock: ratio * budget for stock, ratio in zip(top_tickers, funds_ratios)}

dataframes = []
for ticker in top_tickers:
    ticker_dir = os.path.join(base_dir, ticker)
    df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
    df["Ticker"] = ticker
    dataframes.append(df)

all_data = pd.concat(dataframes)
shares = {stock: funds[stock] / all_data[(all_data["Ticker"] == stock)].iloc[0]["Close"] for stock in top_tickers}

portfolio_value = sum([shares[stock] * all_data[(all_data["Ticker"] == stock)].iloc[-1]["Close"] for stock in top_tickers])

earned = portfolio_value/(budget/100.0)
print(
    f"Final value using this strategy: ${portfolio_value}, which is a %{earned:.2f} return")

json_file_path = 'output.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)

if "stoch" in data["Shares"]:
    data["Shares"]["stoch"].update(shares)
else:
    data["Shares"]["stoch"] = shares

data["stoch"] = earned

for strategy in data["Shares"]:
    data["Shares"][strategy] = {k: v for k, v in sorted(data["Shares"][strategy].items(), key=lambda item: item[1])}

with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=4)
