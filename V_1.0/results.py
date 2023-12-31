import os
import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_thursdays(start_date, end_date):
    start_date = start_date + timedelta((3 - start_date.weekday() + 7) % 7)
    while start_date < end_date:
        yield start_date
        start_date += timedelta(weeks=1)


with open('input/backtest.json', 'r') as f:
    data = json.load(f)

with open('input/input_results.json', 'r') as f:
    dates = json.load(f)

for date_pair in dates:
    start_date = datetime.strptime(date_pair['start'], '%Y-%m-%d')
    end_date = datetime.strptime(date_pair['end'], '%Y-%m-%d')

    results = {}

    for thursday in get_thursdays(start_date, end_date):
        thursday_str = thursday.strftime('%Y-%m-%d')
        results[thursday_str] = {}

        for category, stocks in data['Shares'].items():
            initial_investment = 0
            final_value = 0

            for stock, shares in stocks.items():
                df = yf.download(stock, start=thursday_str, end=(
                    thursday + timedelta(weeks=1)).strftime('%Y-%m-%d'))
                if not df.empty:
                    cost = df.iloc[0]['Close'] * shares
                    sales = df.iloc[-1]['Close'] * shares

                    initial_investment += cost
                    final_value += sales

            if initial_investment != 0:
                percentage_change = (
                    (final_value - initial_investment) / initial_investment) * 100
            else:
                percentage_change = 0

            results[thursday_str][category] = percentage_change

    date_str = date_pair['start'] + '_' + date_pair['end']
    os.makedirs('results', exist_ok=True)
    with open(f'results/results_{date_str}.json', 'w') as f:
        json.dump(results, f, indent=4)
