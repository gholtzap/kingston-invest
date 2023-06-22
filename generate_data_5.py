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

def fetch_data_for_categories(tickers, category):
    print(f'Fetching data for {category}\n')
    chunks = [tickers[i:i + 5] for i in range(0, len(tickers), 5)]

    for i, chunk in enumerate(chunks):
        for ticker in chunk:
            fetch_and_save_data(ticker, category)

        if i < len(chunks) - 1:
            fact = randfacts.get_fact()
            print(f"\nFun fact of the minute: {fact}\n\n1 Minute Cooldown... \n")
            for _ in tqdm(range(61)):
                time.sleep(1)


big_tech_tickers = ['AAPL', 'TSLA', 'MSFT', 'SPOT',
                    'AMZN', 'GOOG', 'ORCL', 'NVDA', 'CSCO', 'META']
cancelled_tickers = ['TGT', 'BUD']
misc_tickers = ['CI', 'SCHW']

fetch_data_for_categories(big_tech_tickers, 'big_tech')

res = quote('Andrew Tate')
try:
    print(f"\nDaily Andrew Tate quote: {res[random.randint(0, len(res))]['quote']}\n")
except IndexError:
    print("\nNo quotes from the Top G available today.\n")
    
for _ in tqdm(range(61)):
    time.sleep(1)
fetch_data_for_categories(cancelled_tickers, 'cancelled')

try:
    res = quote('Warren Buffet')
except IndexError:
    print("\nNo quotes from Warren Buffet available today.\n")


print(f"\nDaily Warren Buffet quote: {res[random.randint(0, len(res))]['quote']}\n")
for _ in tqdm(range(61)):
    time.sleep(1)
fetch_data_for_categories(misc_tickers, 'misc')
