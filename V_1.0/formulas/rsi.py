import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json

base_dir = "../data"

all_data = pd.DataFrame()
dataframes = []

def computeRSI (data, time_window):
    diff = data.diff(1).dropna()        
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[ diff>0 ]
    down_chg[diff < 0] = diff[ diff < 0 ]
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")

        df["RSI"] = computeRSI(df["Close"], 14)

        df["Ticker"] = ticker

        dataframes.append(df)

all_data = pd.concat(dataframes)

all_data = all_data.dropna()

selected_stocks = all_data[(all_data["RSI"] < 30) & (all_data.groupby("Ticker")["RSI"].shift() > 30)]["Ticker"].unique()

print(f"Selected stocks: {selected_stocks}")

budget = 10000

funds = {stock: budget / len(selected_stocks) for stock in selected_stocks}

shares = {stock: funds[stock] / all_data[(all_data["Ticker"] == stock)].iloc[0]["Close"] for stock in selected_stocks}

portfolio_value = sum([shares[stock] * all_data[(all_data["Ticker"]
                      == stock)].iloc[-1]["Close"] for stock in selected_stocks])

earned = portfolio_value/(budget/100.0)
print(
    f"Final value using RSI strategy: ${portfolio_value}, which is a %{earned:.2f} return")


output = ['rsi', earned, shares]

output_dict = {output[0]: output[1], "Shares": output[2]}
if not os.path.isfile('output.json'):
    # If not, create a new dictionary with the desired structure
    data = {
        'Shares': {
            output[0]: output[2]
        },
        output[0]: output[1]
    }
else:
    # If it does, load the existing data
    with open('output.json', 'r') as f:
        data = json.load(f)

    # Update the data dictionary
    data[output[0]] = output[1]
    data['Shares'][output[0]] = output[2]

# Write the updated data back to the file with indentation
with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)