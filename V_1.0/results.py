import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_thursdays(start_date, end_date):
    # Start from the week after the start_date
    start_date = start_date + timedelta((3 - start_date.weekday() + 7) % 7)
    while start_date < end_date:
        yield start_date
        start_date += timedelta(weeks=1)

# Load the data
with open('backtest.json', 'r') as f:
    data = json.load(f)

# The date you bought the stocks
start_date = datetime.strptime('2023-06-21', '%Y-%m-%d')
# The date you sell the stocks (now)
end_date = datetime.now()

results = {}

for thursday in get_thursdays(start_date, end_date):
    thursday_str = thursday.strftime('%Y-%m-%d')
    results[thursday_str] = {}

    for category, stocks in data['Shares'].items():
        # Assume you start with $0
        initial_investment = 0
        final_value = 0

        for stock, shares in stocks.items():
            # Get stock historical data from the Yahoo Finance
            df = yf.download(stock, start=thursday_str, end=(thursday + timedelta(weeks=1)).strftime('%Y-%m-%d'))
            if not df.empty:
                # Calculate the cost and the sales
                cost = df.iloc[0]['Close'] * shares
                sales = df.iloc[-1]['Close'] * shares

                # Update the initial investment and final value
                initial_investment += cost
                final_value += sales

        # Calculate the percentage gain or loss
        if initial_investment != 0:
            percentage_change = ((final_value - initial_investment) / initial_investment) * 100
        else:
            percentage_change = 0

        results[thursday_str][category] = percentage_change

# Save the results to a JSON file
with open('weekly_results.json', 'w') as f:
    json.dump(results, f, indent=4)

