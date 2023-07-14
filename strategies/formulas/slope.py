import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

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
    f"Final value using slope formula: ${portfolio_value}, which is a %{earned:.2f} return")
