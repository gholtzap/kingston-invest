import time
import requests
import os
import csv
from tqdm import tqdm
from dotenv import load_dotenv
import randfacts
import random
from quote import quote

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
        print(f'Fetching data for {category}\n')
        chunks = [tickers[i:i + 5] for i in range(0, len(tickers), 5)]

        for i, chunk in enumerate(chunks):
            for ticker in chunk:
                fetch_and_save_data(ticker, category)

            if i < len(chunks) - 1:
                fact = randfacts.get_fact()
                print(
                    f"\nFun fact of the minute: {fact}\n\n1 Minute Cooldown... \n")
                for _ in tqdm(range(61)):
                    time.sleep(1)


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

res = quote('Andrew Tate')
try:
    print(
        f"\nDaily Andrew Tate quote: {res[random.randint(0, len(res))]['quote']}\n")
except IndexError:
    print("\nNo quotes from the Top G available today.\n")

try:
    res = quote('Warren Buffet')
    print(
        f"\nDaily Warren Buffet quote: {res[random.randint(0, len(res))]['quote']}\n")
except IndexError:
    print("\nNo quotes from Warren Buffet available today.\n")
