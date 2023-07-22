import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json

base_dir = "../data"

all_data = pd.DataFrame()
dataframes = []

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")

        df['Slope'] = np.nan
        df['Day'] = range(len(df))

        for i in range(14, len(df)):
            model = LinearRegression().fit(df[['Day']].iloc[i-14:i], df[['Close']].iloc[i-14:i])
            df.loc[i, 'Slope'] = model.coef_[0][0]

        df["Ticker"] = ticker

        dataframes.append(df)

all_data = pd.concat(dataframes)

all_data = all_data.dropna()

def select_stock(df):
    if any(df['Slope'].iloc[-7:] < 0) and df['Slope'].iloc[-1] >= df['Slope'].iloc[-2]:
        return True
    return False

selected_stocks = [ticker for ticker in all_data['Ticker'].unique() if select_stock(all_data[all_data['Ticker'] == ticker])]

print(f"Selected stocks: {selected_stocks}")

selected_stocks = sorted(selected_stocks, key=lambda x: all_data[all_data["Ticker"] == x].iloc[-1]
                         ["Slope"], reverse=True)[:10]

budget = 10000

# With equal weighting, each stock will get the same allocation.
funds = {stock: budget / len(selected_stocks) for stock in selected_stocks}

shares = {stock: funds[stock] / all_data[(all_data["Ticker"] == stock)].iloc[0]["Close"] for stock in selected_stocks}

portfolio_value = sum([shares[stock] * all_data[(all_data["Ticker"]
                      == stock)].iloc[-1]["Close"] for stock in selected_stocks])

earned = portfolio_value/(budget/100.0)
print(
    f"Final value using nike formula: ${portfolio_value}, which is a %{earned:.2f} return")


output = ['nike', earned, shares]

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