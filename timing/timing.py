import pandas as pd
import os
import yfinance as yf
import bt
from datetime import datetime, timedelta

directory = 'data/'
initial_balance = 10000
portfolio = {}


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


def should_buy_stock(ticker_averages):
    decisions = {}

    for ticker, average in ticker_averages.items():
        data = yf.Ticker(ticker)
        history = data.history(period='1d')
        current_price = history['Close'][0]

        change_needed = average - current_price

        # Calculate the percentage change needed
        percentage_change_needed = (change_needed / current_price) * 100

        if current_price < average:
            decisions[ticker] = ('Buy', change_needed, percentage_change_needed, current_price, average)
        else:
            decisions[ticker] = ('Do not buy', change_needed, percentage_change_needed, current_price, average)

    return decisions


buy_decisions = should_buy_stock(averages)

# Sort by absolute percentage change needed, in ascending order
sorted_decisions = sorted(buy_decisions.items(), key=lambda x: (x[1][0] == 'Do not buy', abs(x[1][2])))

for ticker, (decision, change_needed, percentage_change_needed, current_price, average) in sorted_decisions:
    print(
        f'Ticker: {ticker}, Decision: {decision}, Change Needed: {change_needed}, Percentage Change Needed: {percentage_change_needed:.2f}%')
