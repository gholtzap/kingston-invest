import os
import pandas as pd
import requests
import json
from generate_data import tickers
from dotenv import load_dotenv
import time
import yfinance as yf

load_dotenv()
print(f"\nDIVIDEND_YIELD.PY\n")

totals = {}
API_KEY = os.getenv("AV_API_KEY")


def get_dividend_yield(ticker):
    ticker_info = yf.Ticker(ticker)
    try:
        dy = ticker_info.info['dividendYield'] 
        return dy
    except KeyError:
        print(f"No dividend yield data for {ticker}.")
        return 0 


def dividend_yield(ticker, filename):

    data = pd.read_csv(f'data/{ticker}/{filename}')

    dy = get_dividend_yield(ticker)

    totals[ticker] = dy

    return dy


for ticker in tickers:
    ticker_dir = f'data/{ticker}'
    for filename in os.listdir(ticker_dir):
        dividend_yield(ticker, filename)

num_tickers = 10
top = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:num_tickers]

top_tickers = [item[0] for item in top]

sorted_values = sorted(totals.values(), reverse=True)

print('##################################')
results = []
for stock in top:

    name = stock[0]
    dy = stock[1]

    results.append([name, dy])
