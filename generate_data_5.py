import time
import requests
import os
from dotenv import load_dotenv
import csv
from tqdm import tqdm
import randfacts


load_dotenv()
AV_API_KEY = os.getenv('AV_API_KEY')

################################################################################################
####################################### BIG TECH ###############################################
################################################################################################

# Define a function to fetch and save data
def fetch_and_save_big_tech(ticker):
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
        with open(f'data/big_tech/{ticker}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'close'])
            writer.writerows(csv_data)

        print(f"Data for {ticker} saved to {ticker}.csv")
    else:
        print(f"Error fetching data for {ticker}: {data}")



################################################################################################
####################################### Cancelled ##############################################
################################################################################################

def fetch_and_save_cancelled(ticker):
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
        with open(f'data/cancelled/{ticker}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'close'])
            writer.writerows(csv_data)

        print(f"Data for {ticker} saved to {ticker}.csv")
    else:
        print(f"Error fetching data for {ticker}: {data}")


################################################################################################
####################################### Misc ###################################################
################################################################################################


def fetch_and_save_misc(ticker):
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
        with open(f'data/misc/{ticker}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'close'])
            writer.writerows(csv_data)

        print(f"Data for {ticker} saved to {ticker}.csv")
    else:
        print(f"Error fetching data for {ticker}: {data}")


# Tickers
big_tech_tickers = ['AAPL', 'TSLA', 'MSFT', 'SPOT', 'AMZN', 'GOOG','ORCL']
cancelled_tickers = ['TGT','BUD']
misc_tickers = ['CI','SCHW']

# Split tickers into chunks of 5
big_tech_chunks = [big_tech_tickers[i:i + 5] for i in range(0, len(big_tech_tickers), 5)]
cancelled_chunks = [cancelled_tickers[i:i + 5] for i in range(0, len(cancelled_tickers), 5)]
misc_chunks = [misc_tickers[i:i + 5] for i in range(0, len(misc_tickers), 5)]

# Iterate over each chunk
print('Fetching big tech data')
for i, chunk in enumerate(big_tech_chunks):
    # Fetch and save data for each ticker in chunk
    for ticker in chunk:
        fetch_and_save_big_tech(ticker)

    if i < len(big_tech_chunks) - 1:
        fact = randfacts.get_fact()
        print(f"1 Minute Cooldown... \nFun fact of the minute: {fact}")
        for _ in tqdm(range(61)): 
            time.sleep(1)
        
print('Now fetching Cancelled Data...\n')
print(f"1 Minute Cooldown... \nFun fact of the minute: {fact}")
for _ in tqdm(range(61)): 
        time.sleep(1)
for i, chunk in enumerate(cancelled_chunks):
    # Fetch and save data for each ticker in chunk
    for ticker in chunk:
        fetch_and_save_cancelled(ticker)

    if i < len(cancelled_chunks) - 1:
        fact = randfacts.get_fact()
        print(f"1 Minute Cooldown... \nFun fact of the minute: {fact}")
        for _ in tqdm(range(61)): 
            time.sleep(1)
            
print('Now fetching Misc Data...\n')
print(f"1 Minute Cooldown... \nFun fact of the minute: {fact}")
for _ in tqdm(range(61)): 
        time.sleep(1)
        
for i, chunk in enumerate(misc_chunks):
    # Fetch and save data for each ticker in chunk
    for ticker in chunk:
        fetch_and_save_misc(ticker)

    if i < len(misc_chunks) - 1:
        fact = randfacts.get_fact()
        print(f"1 Minute Cooldown... \nFun fact of the minute: {fact}")
        for _ in tqdm(range(61)): 
            time.sleep(1)