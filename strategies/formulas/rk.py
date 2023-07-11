import os
import pandas as pd
import requests
import json
from generate_data import tickers
from dotenv import load_dotenv
import time

load_dotenv()
print(f"\nFORMULA_RK.PY\n")

totals = {}
API_KEY = os.getenv("AV_API_KEY")


def get_eps(ticker):
    response = requests.get(
        f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}')
    data = json.loads(response.text)
    if 'EPS' in data:
        return float(data['EPS'])
    else:
        print(f"No EPS data for {ticker}. Response: {data}")
        return 0


def formula(ticker, filename):

    data = pd.read_csv(f'data/{ticker}/{filename}')

    price = data['Close'].iloc[-1]
    eps = get_eps(ticker)

    if eps != 0:
        pe_ratio = price / eps
    else:
        pe_ratio = float('inf')

    totals[ticker] = pe_ratio

    return pe_ratio


for ticker in tickers:
    ticker_dir = f'data/{ticker}'
    for filename in os.listdir(ticker_dir):
        print(f"Fetching data for {ticker}")
        formula(ticker, filename)
        time.sleep(12)

num_tickers = 10
top = sorted(totals.items(), key=lambda item: item[1])[:num_tickers]

top_tickers = [item[0] for item in top]

sorted_values = sorted(totals.values())

print('##################################')
results = []
for stock in top:

    name = stock[0]
    pe_ratio = stock[1]

    results.append([name, pe_ratio])
