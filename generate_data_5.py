import time
import requests
import os
from dotenv import load_dotenv
import csv
from tqdm import tqdm
import randfacts


load_dotenv()
AV_API_KEY = os.getenv('AV_API_KEY')

# Define a function to fetch and save data
def fetch_and_save(ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={AV_API_KEY}'
    print(f"Fetching data for {ticker} from {url}")
    r = requests.get(url)
    data = r.json()

    if 'Time Series (Daily)' in data:
        # Prepare data for CSV
        csv_data = []
        for date, values in data['Time Series (Daily)'].items():
            csv_data.append([date, values['4. close']])

        # Write to CSV
        with open(f'data/{ticker}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'close'])
            writer.writerows(csv_data)

        print(f"Data for {ticker} saved to {ticker}.csv")
    else:
        print(f"Error fetching data for {ticker}: {data}")

# Your list of tickers
big_tech = ['AAPL', 'TSLA', 'MSFT', 'SPOT', 'AMZN', 'GOOG','ORCL']
cancelled = ['TGT','BUD']
tickers = big_tech+cancelled

# Split tickers into chunks of 5
chunks = [tickers[i:i + 5] for i in range(0, len(tickers), 5)]

# Iterate over each chunk
for i, chunk in enumerate(chunks):
    # Fetch and save data for each ticker in chunk
    for ticker in chunk:
        fetch_and_save(ticker)

    # Sleep for 60 seconds before fetching the next chunk
    # if this is not the last chunk
    if i < len(chunks) - 1:
        fact = randfacts.get_fact()
        print(f"1 Minute Cooldown... \nFun fact of the minute: {fact}")
        for _ in tqdm(range(61)): 
            time.sleep(1)