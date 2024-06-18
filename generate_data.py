import time
import os
import csv
import json
from tqdm import tqdm
from datetime import datetime, timedelta
import yfinance as yf
import logging
import coloredlogs

# Set up logging with coloredlogs
coloredlogs.install(level='INFO')
logging.basicConfig(level=logging.INFO)

def fetch_and_save_data(ticker, months):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30*months)

    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if data.empty:
        logging.error(f"Error fetching data for {ticker}")
        return

    data = data.reset_index()
    csv_data = data[['Date', 'Close']].copy()
    csv_data['Date'] = csv_data['Date'].dt.strftime('%Y-%m-%d')

    dir_path = f'data/stocks-{months}m'
    os.makedirs(dir_path, exist_ok=True)

    with open(f'{dir_path}/{ticker}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'close'])
        writer.writerows(csv_data.values)

    logging.info(f"Data for {ticker} saved to {ticker}.csv")


def remove_unwanted_tickers_files(tickers, months_list):
    for months in months_list:
        dir_path = f'data/stocks-{months}m'
        if not os.path.exists(dir_path):
            continue

        for filename in os.listdir(dir_path):
            ticker_filename = os.path.splitext(filename)[0]
            if ticker_filename not in tickers:
                os.remove(os.path.join(dir_path, filename))
                logging.info(f"Deleted data for {ticker_filename} {months}m as it does not exist in tickers.json")


def fetch_data_for_tickers(tickers, months):
    logging.info(f'Fetching data for tickers over past {months} months')

    for ticker in tickers:
        fetch_and_save_data(ticker, months)


with open('tickers.json') as f:
    data = json.load(f)

fetch_data_for_tickers(data['tickers'], 12)
remove_unwanted_tickers_files(data['tickers'], [12,48])
print("\n")