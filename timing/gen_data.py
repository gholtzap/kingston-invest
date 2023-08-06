import os
import pandas as pd
from datetime import datetime, timedelta
import shutil
import json
import finnhub
import numpy as np
import time
import traceback
from dotenv import load_dotenv

print(f"\nGEN_DATA.PY\n")

# Load API key from .env file
load_dotenv()
finnhub_api_key = os.getenv('FINNHUB_API_KEY')

# Set up client
finnhub_client = finnhub.Client(api_key=finnhub_api_key)



with open("tickers.json") as f:
    tickers_json = json.load(f)

tickers = tickers_json['tickers']

folders = os.listdir('data')
for folder in folders:
    if folder not in tickers:
        shutil.rmtree(f'data/{folder}')

start_date = datetime.now() - timedelta(days=2*365)
end_date = datetime.now()



if not os.path.exists('data'):
    os.makedirs('data')


for ticker in tickers:
    try:
        res = finnhub_client.stock_candles(ticker, 'D', int(start_date.timestamp()), int(end_date.timestamp()))
        
        # Create a datetime index using the timestamps from the response
        timestamps = pd.to_datetime(res['t'], unit='s')
        
        # Create a DataFrame using the close prices and the datetime index
        df = pd.DataFrame({'Close': res['c']}, index=timestamps)
        print(f"Data for {ticker}:\n{df.head()}")
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
        traceback.print_exc()
    time.sleep(1)
    df = df.resample('D').ffill()

    six_month_intervals = pd.date_range(
        start=start_date, end=end_date, freq='6M')

    if six_month_intervals[-1] != end_date:
        six_month_intervals = six_month_intervals.append(
            pd.to_datetime([end_date]))

    ticker_dir = f'data/{ticker}'
    if not os.path.exists(ticker_dir):
        os.makedirs(ticker_dir)

    for i in range(len(six_month_intervals) - 1):
        start_interval = six_month_intervals[i]
        end_interval = six_month_intervals[i+1]

        df_interval = df.loc[start_interval:end_interval]

        # Reset the index so the dates become a regular column
        df_interval.reset_index(inplace=True)

        # Rename the index column to 'Date'
        df_interval.rename(columns={'index': 'Date'}, inplace=True)

        df_interval.to_csv(
            f'{ticker_dir}/{ticker}_{start_interval.date()}_{end_interval.date()}.csv', index=False)

    # Reset the index for the full DataFrame and rename the index column to 'Date'
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)

    df.to_csv(f'{ticker_dir}/{ticker}_2_year_data.csv', index=False)
