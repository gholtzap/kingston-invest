import os
import pandas as pd
import json
import requests
from dotenv import load_dotenv
from tqdm import tqdm
import time

load_dotenv()
API_KEY = os.getenv('FINNHUB_API_KEY')
base_dir = "../data"

all_data = pd.DataFrame()
dataframes = []

for ticker in os.listdir(base_dir):
    ticker_dir = os.path.join(base_dir, ticker)

    if os.path.isdir(ticker_dir):
        df = pd.read_csv(f"{ticker_dir}/{ticker}_5_year_data.csv")
        print(f"Fetching data for {ticker}")

        eps_response = requests.get(
            f"https://finnhub.io/api/v1/stock/earnings?symbol={ticker}&token={API_KEY}")
        eps_data = eps_response.json()
        print(eps_data)

        market_cap_response = requests.get(
            f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}")
        market_cap_data = market_cap_response.json()
        print(market_cap_data)

        for _ in tqdm(range(1)):
            time.sleep(1)
        
        if eps_data and 'c' in market_cap_data:  
            df["EPS"] = eps_data[0]['actual']
            df["Price"] = market_cap_data['c']
            df["PE_ratio"] = df["Price"] / df["EPS"]
            df["Ticker"] = ticker
            dataframes.append(df)
            print(f"Dataframe for {ticker}: {df}")

if dataframes:
    all_data = pd.concat(dataframes)
    all_data = all_data.dropna()
else:
    print("No data to process.")
    exit()




if eps_data and 'c' in market_cap_data: 
    df["EPS"] = eps_data[0]['actual']
    df = df.sort_values("Date")
    df = df.reset_index(drop=True)

    df.loc[0, "PE_ratio"] = df.loc[0, "Close"] / df.loc[0, "EPS"]
    
    df.loc[len(df) - 1, "PE_ratio"] = df.loc[len(df) - 1, "Close"] / df.loc[len(df) - 1, "EPS"]

    df["Ticker"] = ticker
    dataframes.append(df)


if dataframes: 
    all_data = pd.concat(dataframes)
    all_data = all_data.dropna()
else:
    print("No data to process.")
    exit()

selected_stocks = all_data.sort_values(
    by="PE_ratio").groupby("Ticker").first().sort_values(
    by="PE_ratio", ascending=True).index[:10]

budget = 10000
total_ratio = sum([1.61803398875**i for i in range(10)])

funds = {stock: budget * (1.61803398875**i / total_ratio)
         for i, stock in enumerate(selected_stocks)}

initial_prices = {stock: all_data[(all_data["Ticker"]
                                   == stock)].iloc[0]["Close"] for stock in selected_stocks}

final_prices = {stock: all_data[(all_data["Ticker"]
                                 == stock)].iloc[-1]["Close"] for stock in selected_stocks}

shares = {stock: funds[stock] / initial_prices[stock] for stock in selected_stocks}

portfolio_value = sum([shares[stock] * final_prices[stock] for stock in selected_stocks])

earned = portfolio_value / (budget / 100.0)
print(
    f"Final value using P/E ratio and EPS formula: ${portfolio_value}, which is a %{earned:.2f} return")
output = ['rk', earned, shares]

output_dict = {output[0]: output[1], "Shares": output[2]}

if not os.path.isfile('output.json'):
    data = {
        'Shares': {
            output[0]: output[2]
        },
        output[0]: output[1]
    }
else:
    with open('output.json', 'r') as f:
        data = json.load(f)

    data[output[0]] = output[1]
    data['Shares'][output[0]] = output[2]

with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)
