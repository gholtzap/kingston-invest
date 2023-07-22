import time
import requests
import os
import csv
import json
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
AV_API_KEY = os.getenv('AV_API_KEY')

def fetch_and_save_data(ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={AV_API_KEY}'
    r = requests.get(url)
    data = r.json()

    if 'Time Series (Daily)' not in data:
        print(f"Error fetching data for {ticker}: {data}")
        return

    csv_data = [[date, values['4. close']]
                for date, values in data['Time Series (Daily)'].items()]

    with open(f'data/{ticker}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'close'])
        writer.writerows(csv_data)

    print(f"Data for {ticker} saved to {ticker}.csv")


def fetch_data_for_tickers(tickers):
    print(f'Fetching data for tickers\n')

    for ticker in tickers:
        for _ in tqdm(range(12)):
                time.sleep(1)
        fetch_and_save_data(ticker)


with open('tickers.json') as f:
    data = json.load(f)

fetch_data_for_tickers(data['tickers'])
