import os
import pandas as pd
import pprint
from generate_data import tickers

print(f"\nRUNNING FORMULA_IMAN\n")

totals = {}
sma = {}


def formula(ticker, filename):

    data = pd.read_csv(f'data/{ticker}/{filename}')

    avg_price = data['Close'].mean()

    data['PctChange'] = data['Close'].pct_change()

    volatility = data['PctChange'].std() * (365 ** 0.5)

    score = 1 / volatility

    if ticker not in totals:
        totals[ticker] = [score, avg_price]

        sma[ticker] = [avg_price]
    else:
        totals[ticker][0] += score
        totals[ticker][1] += avg_price
        totals[ticker][1] /= 2

        sma[ticker] += [avg_price]
        sma[ticker].sort()

    return score


for ticker in tickers:
    ticker_dir = f'data/{ticker}'
    for filename in os.listdir(ticker_dir):
        formula(ticker, filename)


num_tickers = 10
top = sorted(totals.items(), key=lambda item: item[1], reverse=True)[
    :num_tickers]

top_tickers = [item[0] for item in top]

sorted_values = sorted(totals.values(), reverse=True)

print('##################################')
results = []
for stock in top:

    name = stock[0]
    score = stock[1][0]
    avg_price = stock[1][1]

    obj = sma[name]
    bar = obj[1]
    results.append([name, bar])
