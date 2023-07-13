import os
import pandas as pd

base_dir = "../data"

all_data = pd.DataFrame()
dataframes = []

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")

        df["MA50"] = df["Close"].rolling(window=50).mean()
        df["MA200"] = df["Close"].rolling(window=200).mean()

        df["Ticker"] = ticker

        dataframes.append(df)

all_data = pd.concat(dataframes)

all_data = all_data.dropna()

selected_stocks = all_data[all_data["MA50"]
                           > all_data["MA200"]]["Ticker"].unique()

selected_stocks = sorted(selected_stocks, key=lambda x: all_data[all_data["Ticker"] == x].iloc[-1]
                         ["MA50"] - all_data[all_data["Ticker"] == x].iloc[-1]["MA200"], reverse=True)[:10]

budget = 10000

total_ratio = sum([1.61803398875**i for i in range(10)])

funds = {stock: budget * (1.61803398875**i / total_ratio)
         for i, stock in enumerate(selected_stocks)}

shares = {stock: funds[stock] / all_data[(
    all_data["Ticker"] == stock)].iloc[0]["Close"] for stock in selected_stocks}

portfolio_value = sum([shares[stock] * all_data[(all_data["Ticker"]
                      == stock)].iloc[-1]["Close"] for stock in selected_stocks])

earned = portfolio_value/(budget/100.0)
print(
    f"Final value using MA formula: ${portfolio_value}, which is a %{earned:.2f} return")
