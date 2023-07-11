import os
import pandas as pd
from generate_data import tickers

print(f"\nRUNNING FORMULA_DIWI\n")

totals = {}
sma = {}

def formula(ticker, filename):

    data = pd.read_csv(f'data/{ticker}/{filename}')

    data['PctChange'] = data['Close'].pct_change()

    data['30DaySMA'] = data['Close'].rolling(window=30).mean()

    data['HardDip'] = data['Close'] < (data['30DaySMA'] * 0.8)

    hard_dips = data[data['HardDip']].shape[0]

    if ticker not in totals:
        totals[ticker] = [hard_dips]
    else:
        totals[ticker][0] += hard_dips

    return hard_dips


for ticker in tickers:
    ticker_dir = f'data/{ticker}'
    for filename in os.listdir(ticker_dir):
        formula(ticker, filename)


num_tickers = 10
top = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:num_tickers]

top_tickers = [item[0] for item in top]

print('##################################')
results = []
for stock in top:
    name = stock[0]
    hard_dips = stock[1][0]
    results.append([name, hard_dips])
