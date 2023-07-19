import time
import requests
import os
import csv
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
AV_API_KEY = os.getenv('AV_API_KEY')


def fetch_and_save_data(ticker, category):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={AV_API_KEY}'
    r = requests.get(url)
    data = r.json()

    if 'Time Series (Daily)' not in data:
        print(f"Error fetching data for {ticker}: {data}")
        return

    csv_data = [[date, values['4. close']]
                for date, values in data['Time Series (Daily)'].items()]

    with open(f'data/{category}/{ticker}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'close'])
        writer.writerows(csv_data)

    print(f"Data for {ticker} saved to {ticker}.csv")


def fetch_data_for_categories(category_tickers):
    for category, tickers in category_tickers.items():
        print(f"TICKERS {tickers}")
        
                    
        print(f'Fetching data for {category}\n')

        for ticker in tickers:
            for _ in tqdm(range(12)):
                    time.sleep(1)
            fetch_and_save_data(ticker, category)


big_tech_tickers = ['AAPL', 'TSLA', 'MSFT', 'SPOT',
                    'AMZN', 'GOOG', 'ORCL', 'NVDA', 'CSCO', 'META', 'INTU', 'ADBE']
cancelled_tickers = ['TGT', 'BUD']
misc_tickers = ['CI', 'SCHW']
new_test_category = ['JPM']

tickers = {}

ticker_categories = ['big_tech_tickers',
                     'cancelled_tickers', 'misc_tickers', 'new_test_category']


for category in ticker_categories:
    for ticker in globals()[category]:
        tickers[ticker] = category

print(tickers)


ticker_categories = {
    'big_tech': big_tech_tickers,
    'cancelled': cancelled_tickers,
    'misc': misc_tickers,
    'new_test_category': new_test_category
}

fetch_data_for_categories(ticker_categories)