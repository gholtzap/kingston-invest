import os
import pandas as pd
import requests
import json
import time
from dotenv import load_dotenv


load_dotenv()

base_dir = "../data"

AV_API_KEY = os.getenv("AV_API_KEY")
AV_API_URL = "https://www.alphavantage.co/query"


def get_eps(ticker):
    print(f"Fetching data for {ticker}")
    data = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": AV_API_KEY,
    }
    response = requests.get(AV_API_URL, data)
    result = json.loads(response.text)
    time.sleep(12.02)
    try:
        eps = result['EPS']
        return float(eps)
    except KeyError:
        print(f"No EPS data for {ticker}.")
        return 0


def calculate_score(ticker, price):
    eps = get_eps(ticker)
    if eps != 0:
        pe_ratio = price / eps
    else:
        pe_ratio = float('inf')
    return pe_ratio


def backtest():
    budget_per_stock = 1000  # assuming an initial budget of $10000, and we will invest $1000 in each stock
    total_value = 0
    for year in range(2019, 2022):
        scores = {}
        for ticker in os.listdir(base_dir):
            ticker_dir = os.path.join(base_dir, ticker)
            if os.path.isdir(ticker_dir):
                df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                start_price = df.loc[str(year)]['Close'].iloc[0]
                scores[ticker] = (start_price, calculate_score(ticker, start_price))
        
        # Select top 10 stocks
        top_stocks = sorted(scores.items(), key=lambda item: item[1][1])[:10]
        
        # Calculate end of year value
        for stock in top_stocks:
            ticker = stock[0]
            start_price = stock[1][0]
            df = pd.read_csv(f"{base_dir}/{ticker}/{ticker}_5_year_data.csv")
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            end_price = df.loc[str(year)]['Close'].iloc[-1]
            num_shares = budget_per_stock / start_price
            total_value += num_shares * end_price
    
    return total_value


total_value = backtest()
print(f"Final portfolio value after 5 years: ${total_value}")
