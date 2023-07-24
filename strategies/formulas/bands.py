import os
import pandas as pd
import numpy as np
import json

base_dir = "../data"
totals = {}

def calculate_score(data):
    data['Close20DaySMA'] = data['Close'].rolling(window=20).mean()
    data['StdDev'] = data['Close'].rolling(window=20).std()
    data['LowerBand'] = data['Close20DaySMA'] - (2 * data['StdDev'])
    data['UpperBand'] = data['Close20DaySMA'] + (2 * data['StdDev'])
    data['BuySignal'] = data['Close'] < data['LowerBand']
    buy_signals = data[data['BuySignal']].shape[0]
    return buy_signals

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
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

if "boll" in data["Shares"]:
    data["Shares"]["boll"].update(shares)
else:
    data["Shares"]["boll"] = shares

data["boll"] = earned

for strategy in data["Shares"]:
    data["Shares"][strategy] = {k: v for k, v in sorted(data["Shares"][strategy].items(), key=lambda item: item[1])}

with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=4)
