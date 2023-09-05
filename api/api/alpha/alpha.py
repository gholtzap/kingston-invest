import os
import pandas as pd
from datetime import datetime, timedelta
import json
import finnhub
import yfinance as yf
from dotenv import load_dotenv
import time
import traceback

# Load API key from .env file
load_dotenv()
finnhub_api_key = os.getenv('FINNHUB_API_KEY')

# Set up client
finnhub_client = finnhub.Client(api_key=finnhub_api_key)


def calculate_decisions(tickers):
    start_date = datetime.now() - timedelta(days=2*365)
    end_date = datetime.now()

    stock_data = {}

    for ticker in tickers:
        try:
            res = finnhub_client.stock_candles(ticker, 'D', int(start_date.timestamp()), int(end_date.timestamp()))
            timestamps = pd.to_datetime(res['t'], unit='s')
            df = pd.DataFrame({'Close': res['c']}, index=timestamps)
            df = df.resample('D').ffill()

            stock_data[ticker] = df

            print(f"Data for {ticker}:\n{df.head()}")
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
            traceback.print_exc()
        time.sleep(1)

    averages = calc_2q(stock_data)

    buy_decisions = should_buy_stock(averages)

    sorted_decisions = sorted(buy_decisions.items(), key=lambda x: (x[1][0] == 'Do not buy', abs(x[1][1])))

    results = []

    for ticker, (decision, change_needed, current_price, average) in sorted_decisions:
        result = {
            'ticker': ticker,
            'decision': decision,
            'change_needed': change_needed,
            'current_price': current_price,
            'average': average,
        }
        results.append(result)

    return results


def calc_2q(stock_data):
    ticker_averages = {}

    for ticker, df in stock_data.items():
        df['Date'] = df.index
        df.set_index('Date', inplace=True)

        resampled_df = df.resample('6M').mean(numeric_only=True)

        second_lowest_average = resampled_df['Close'].nsmallest(2).iloc[-1]

        ticker_averages[ticker] = second_lowest_average

    return ticker_averages


def should_buy_stock(ticker_averages):
    decisions = {}

    for ticker, average in ticker_averages.items():
        data = yf.Ticker(ticker)
        history = data.history(period='1d')
        current_price = history['Close'][0]

        change_needed = average - current_price

        if current_price < average:
            decisions[ticker] = ('Buy', change_needed, current_price, average)
        else:
            decisions[ticker] = ('Do not buy', change_needed, current_price, average)

    return decisions
