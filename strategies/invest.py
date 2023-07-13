from formulas.iman import results as iman_results
from formulas.diwi import results as diwi_results
from formulas.rk import results as rk_results
from formulas.dy import results as dy_results
import pprint
import operator
import os
import pandas as pd
import math
import json

with open("funds.json") as f:
    funds_json = json.load(f)

funds = funds_json['funds']

print(f"\nINVEST.PY\n")

strategies = {
    "Iman": iman_results,
    "Diwi": diwi_results,
    "RK": rk_results,
    "DY":dy_results
}


def get_investment_plan(stocks, funds):
    total_deviation = sum([price for name, price in stocks])
    stock_scores = {name: price/total_deviation for name, price in stocks}
    investment_plan = {name: funds*score for name,
                       score in stock_scores.items()}
    sorted_investment_plan = dict(
        sorted(investment_plan.items(), key=operator.itemgetter(1), reverse=True))

    return sorted_investment_plan


def backtest_investment_plan(investment_plan):
    total_return = 0
    for stock, investment in investment_plan.items():
        filepath = os.path.join("data", stock, f"{stock}_5_year_data.csv")
        df = pd.read_csv(filepath)

        prices = df['Close']

        shares_bought = investment / prices.iloc[0]
        cost = shares_bought * prices.iloc[0]

        end_value = shares_bought * prices.iloc[-1]

        stock_return = end_value - cost

        total_return += stock_return

    return total_return


percentage_returns = {}

for strategy_name, strategy_results in strategies.items():
    print(f"\nTesting strategy: {strategy_name}\n")
    #pprint.pprint(strategy_results)

    investment_plan = get_investment_plan(strategy_results, funds)

    print(f"\nINVESTMENT PLAN for {strategy_name} BASED ON ${funds} FUNDS\n")
    for stock, investment in investment_plan.items():
        print(f"Invest ${investment:.2f} in {stock}.")

    total_return = backtest_investment_plan(investment_plan)
    percentage_returns[strategy_name] = str(round(total_return/100000,2))
    print(
        f"\nTotal return using {strategy_name}: ${total_return:.2f}, which is a %{100 * (total_return/funds):.2f} return\n")

print(f"###########################\n{percentage_returns}\n###########################")