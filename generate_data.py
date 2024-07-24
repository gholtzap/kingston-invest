import time
import os
import csv
import json
from tqdm import tqdm
from datetime import datetime, timedelta
import yfinance as yf
import logging
import coloredlogs
import socket

# Set up logging with coloredlogs
coloredlogs.install(level='INFO')
logging.basicConfig(level='INFO')

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Check if the internet connection is available.
    Tries to connect to Google's public DNS server (8.8.8.8) on port 53.
    """
    logging.info("Checking Internet Connection [8.8.8.8 - Port 53]")
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logging.info("Connected to Internet")
        return True
    except socket.error as ex:
        logging.error("No internet connection available. Please check your connection.")
        return False

def fetch_and_save_data(ticker, months, folder):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30*months)

    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if data.empty:
        logging.error(f"Error fetching data for {ticker}")
        return

    data = data.reset_index()
    csv_data = data[['Date', 'Close']].copy()
    csv_data['Date'] = csv_data['Date'].dt.strftime('%Y-%m-%d')

    dir_path = f'data/{folder}/stocks-{months}m'
    os.makedirs(dir_path, exist_ok=True)

    with open(f'{dir_path}/{ticker}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'close'])
        writer.writerows(csv_data.values)

    logging.info(f"Data for {ticker} saved to {ticker}.csv in {folder} folder")

def remove_unwanted_tickers_files(tickers, months_list, folder):
    for months in months_list:
        dir_path = f'data/{folder}/stocks-{months}m'
        if not os.path.exists(dir_path):
            continue

        for filename in os.listdir(dir_path):
            ticker_filename = os.path.splitext(filename)[0]
            if ticker_filename not in tickers:
                os.remove(os.path.join(dir_path, filename))
                logging.info(f"Deleted data for {ticker_filename} {months}m in {folder} folder as it does not exist in {folder}.json")

def fetch_data_for_tickers(tickers, months_list, folder):
    for months in months_list:
        logging.info(f'Fetching data for tickers in {folder} folder over past {months} months')

        for ticker in tickers:
            fetch_and_save_data(ticker, months, folder)

def process_json_file(json_file, months_list, folder):
    with open(json_file) as f:
        data = json.load(f)
    
    fetch_data_for_tickers(data['tickers'], months_list, folder)
    remove_unwanted_tickers_files(data['tickers'], months_list, folder)

if check_internet_connection():
    # Process 'tickers_amun.json'
    process_json_file('tickers_amun.json', [12, 48], 'amun')

    # Process 'tickers_anubis.json'
    process_json_file('tickers_anubis.json', [12, 48], 'anubis')
else:
    logging.error("Script terminated due to lack of internet connection.")
