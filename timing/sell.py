import pandas as pd
import os
import yfinance as yf
import bt
from datetime import datetime, timedelta
import pprint
import requests
from dotenv import load_dotenv

directory = 'data/'
initial_balance = 10000
portfolio = {}


load_dotenv()
finnhub_api_key = os.getenv('FINNHUB_API_KEY')

def calc_2q(directory):
    ticker_averages = {}
    for ticker in os.listdir(directory):
        if not os.path.isdir(os.path.join(directory, ticker)):
            continue
        for file in os.listdir(os.path.join(directory, ticker)):
            if file.endswith('.csv'):
                file_path = os.path.join(directory, ticker, file)
                df = pd.read_csv(file_path)
                df['date'] = pd.to_datetime(df['Date'])
                df.set_index('date', inplace=True)
                resampled_df = df.resample('6M').mean(numeric_only=True)
                second_lowest_average = resampled_df['Close'].nsmallest(
                    2).iloc[-1]
                ticker_averages[ticker] = second_lowest_average
    return ticker_averages


averages = calc_2q(directory)


def forecast(ticker):
    output = 1
    
    return output

def market_cap(ticker):
    print(f"CALC MARKET CAP FOR {ticker}")
    data = yf.Ticker(ticker)
    market_cap_value = data.info['marketCap']
    print(f"{ticker} DATA RETRIEVED")

    # Normalize the market cap to a score between 0-100.
    # You may need to replace these values with appropriate bounds for your stocks.
    min_market_cap = 1000000000  # Example of a minimum market cap
    max_market_cap = 1000000000000  # Example of a maximum market cap
    score = ((market_cap_value - min_market_cap) / (max_market_cap - min_market_cap)) * 100

    print(f"{ticker} MARKET CAP {max(0,min(score,100))}")
    return max(0, min(score, 100))  # Clamping the value to be between 0 and 100


def market_cap_f(ticker):
    print(f"FINNHUB MARKET CAP CALC FOR {ticker}")
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={finnhub_api_key}"
    response = requests.get(url)
    market_cap_value = response.json()['metric']['marketCapitalization']

    # Normalize the market cap to a score between 0-100.
    min_market_cap = 1000000000  # Example of a minimum market cap
    max_market_cap = 1000000000000  # Example of a maximum market cap
    score = ((market_cap_value - min_market_cap) / (max_market_cap - min_market_cap)) * 100

    return max(0, min(score, 100))  # Clamping the value to be between 0 and 100

def should_sell_stock(ticker_averages, threshold_pct=35):
    decisions = {}

    for ticker, average in ticker_averages.items():
        print(f"\tDECIDING IF {ticker} BUY OR NOT")
        forecast_pct = forecast(ticker)
        market_cap_pct = market_cap(ticker)
        data = yf.Ticker(ticker)
        history = data.history(period='1d')
        current_price = history['Close'][0]

        change_needed = current_price - average

        percentage_change_needed = (change_needed / average) * 100
        
        # Takes into account raw threshold, market cap, and forecast
        adjusted_threshold_pct = threshold_pct - (forecast_pct * 0.5) + (market_cap_pct * 0.3)

        if current_price > average and percentage_change_needed > adjusted_threshold_pct:
            decisions[ticker] = (
                'Sell', change_needed, percentage_change_needed, current_price, average)
        else:
            decisions[ticker] = ('Don\'t sell', change_needed,
                                 percentage_change_needed, current_price, average)
    return decisions


sell_decisions = should_sell_stock(averages)
sorted_decisions = sorted(sell_decisions.items(), key=lambda x: (
    x[1][0] == 'Don\'t sell', -x[1][2] if x[1][0] == 'Sell' else x[1][2]))
print("{:<10} {:<15} {:<20} {:<15}".format(
    'Ticker', 'Decision', '% Change Needed', '$ Change Needed'))
print("="*60)
for ticker, (decision, change_needed, percentage_change_needed, current_price, average) in sorted_decisions:
    print("{:<10} {:<15} {:<20.2f} {:<15.2f}".format(
        ticker, decision, percentage_change_needed, change_needed))
