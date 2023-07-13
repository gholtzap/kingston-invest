import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import shutil
import json

print(f"\nGENERATE_DATA.PY\n")


with open("tickers.json") as f:
    tickers_json = json.load(f)

tickers = tickers_json['tickers']

folders = os.listdir('data')
for folder in folders:
    if folder not in tickers:
        shutil.rmtree(f'data/{folder}')

start_date = datetime.now() - timedelta(days=5*365)
end_date = datetime.now()

if not os.path.exists('data'):
    os.makedirs('data')

for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)

    df = df[['Close']]

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

        df_interval.to_csv(
            f'{ticker_dir}/{ticker}_{start_interval.date()}_{end_interval.date()}.csv')

    df.to_csv(f'{ticker_dir}/{ticker}_5_year_data.csv')
