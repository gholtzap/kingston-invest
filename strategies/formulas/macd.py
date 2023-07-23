import os
import pandas as pd
import numpy as np
import json

base_dir = "../data"

all_data = pd.DataFrame()
dataframes = []

def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

def calculate_macd(data, short_window, long_window):
    short_ema = calculate_ema(data, short_window)
    long_ema = calculate_ema(data, long_window)
    macd_line = short_ema - long_ema
    signal_line = calculate_ema(macd_line, 9)
    return macd_line, signal_line

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")

        df['MACD'], df['Signal'] = calculate_macd(df['Close'], 12, 26)

        df["Ticker"] = ticker

        dataframes.append(df)

all_data = pd.concat(dataframes)

all_data = all_data.dropna()

selected_stocks = all_data[((all_data["MACD"] > all_data["Signal"]) &
                            (all_data.groupby("Ticker")["MACD"].shift() < all_data.groupby("Ticker")["Signal"].shift()))]["Ticker"].unique()

selected_stocks = sorted(selected_stocks)[:6] # Selects the first 6 stocks alphabetically
print(f"Selected stocks: {selected_stocks}")

budget = 10000

funds_ratios = [0.38, 0.26, 0.12, 0.08, 0.08, 0.08]
funds = {stock: ratio * budget for stock, ratio in zip(selected_stocks, funds_ratios)}

shares = {stock: funds[stock] / all_data[(all_data["Ticker"] == stock)].iloc[0]["Close"] for stock in selected_stocks}

portfolio_value = sum([shares[stock] * all_data[(all_data["Ticker"]
                      == stock)].iloc[-1]["Close"] for stock in selected_stocks])

earned = portfolio_value/(budget/100.0)
print(
    f"Final value using MACD strategy: ${portfolio_value}, which is a %{earned:.2f} return")

output = ['macd', earned, shares]

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
