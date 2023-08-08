import time
import requests
import os
import csv
import json
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')


def fetch_and_save_data(ticker, months):
    from_timestamp = int(
        (datetime.now() - timedelta(days=30*months)).timestamp())

    url = f'https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=D&from={from_timestamp}&to={int(datetime.now().timestamp())}&token={FINNHUB_API_KEY}'
    r = requests.get(url)
    data = r.json()

    if 'c' not in data:
        print(f"Error fetching data for {ticker}: {data}")
        return

    dates = [datetime.utcfromtimestamp(ts).strftime(
        '%Y-%m-%d') for ts in data['t']]
    csv_data = list(zip(dates, data['c']))

    dir_path = f'data/stocks-{months}m'
    os.makedirs(dir_path, exist_ok=True)

    with open(f'{dir_path}/{ticker}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'close'])
        writer.writerows(csv_data)

    print(f"Data for {ticker} saved to {ticker}.csv")

def remove_unwanted_tickers_files(tickers, months_list):
    for months in months_list:
        dir_path = f'data/stocks-{months}m'
        if not os.path.exists(dir_path):
            continue

        for filename in os.listdir(dir_path):
            ticker_filename = os.path.splitext(filename)[0]
            if ticker_filename not in tickers:
                os.remove(os.path.join(dir_path, filename))
                print(f"Deleted data for {ticker_filename} as it does not exist in tickers.json")


def fetch_data_for_tickers(tickers, months):
    print(f'Fetching data for tickers over past {months} months\n')

    for ticker in tickers:
        for _ in tqdm(range(1)):
            time.sleep(1)
        fetch_and_save_data(ticker, months)


with open('tickers.json') as f:
    data = json.load(f)
with open('tickers.json') as f:
    data = json.load(f)

fetch_data_for_tickers(data['tickers'], 6)
fetch_data_for_tickers(data['tickers'], 12)
remove_unwanted_tickers_files(data['tickers'], [6, 12])