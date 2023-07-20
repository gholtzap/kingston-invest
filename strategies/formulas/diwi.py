import os
import pandas as pd
import numpy as np
import json

base_dir = "../data"
totals = {}
sma = {}

def calculate_score(data):
    data['PctChange'] = data['Close'].pct_change()
    data['30DaySMA'] = data['Close'].rolling(window=30).mean()
    data['HardDip'] = data['Close'] < (data['30DaySMA'] * 0.8)
    hard_dips = data[data['HardDip']].shape[0]
    return hard_dips

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
        hard_dips = calculate_score(df)
        totals[ticker] = hard_dips

num_tickers = 10
top = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:num_tickers]
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

# Specify the file path where you want to save your JSON file
json_file_path = 'output.json'

# Read existing data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Append new data to the 'Shares' key
if "diwi" in data["Shares"]:
    data["Shares"]["diwi"].update(shares)
else:
    data["Shares"]["diwi"] = shares

# Append return to the top level of the dictionary
data["diwi"] = earned

# Write back to the file
with open(json_file_path, 'w') as file:
    json.dump(data, file)
