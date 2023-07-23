import time
import requests
import os
import csv
import json
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

def fetch_and_save_data(ticker):
    url = f'https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=D&count=100&token={FINNHUB_API_KEY}'
    r = requests.get(url)
    data = r.json()

    if 'c' not in data:
        print(f"Error fetching data for {ticker}: {data}")
        return

    csv_data = list(zip(data['t'], data['c']))

    with open(f'data/{ticker}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'close'])
        writer.writerows(csv_data)

    print(f"Data for {ticker} saved to {ticker}.csv")


def fetch_data_for_tickers(tickers):
    print(f'Fetching data for tickers\n')

    for ticker in tickers:
        for _ in tqdm(range(1)):
                time.sleep(1)
        fetch_and_save_data(ticker)


with open('tickers.json') as f:
    data = json.load(f)

fetch_data_for_tickers(data['tickers'])
