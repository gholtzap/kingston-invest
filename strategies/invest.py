from formulas.formula_stable import results as stable_results
import pprint
import operator
import os
import pandas as pd
import math

funds = 100000

print(f"\nINVEST.PY\n")

pprint.pprint(stable_results)


def get_investment_plan(stocks, funds):
    total_deviation = sum([price for name, price in stocks])
    stock_scores = {name: price/total_deviation for name, price in stocks}
    investment_plan = {name: funds*score for name,
                       score in stock_scores.items()}
    sorted_investment_plan = dict(
        sorted(investment_plan.items(), key=operator.itemgetter(1), reverse=True))

    return sorted_investment_plan




investment_plan = get_investment_plan(stable_results, funds)

print(f"\nINVESTMENT PLAN BASED ON ${funds} FUNDS\n")

for stock, investment in investment_plan.items():
    print(f"Invest ${investment:.2f} in {stock}.")


def backtest_investment_plan(investment_plan):
    total_return = 0
    for stock, investment in investment_plan.items():
        filepath = os.path.join("data", stock, f"{stock}_2_year_data.csv")
        df = pd.read_csv(filepath)

        prices = df['Close']

        shares_bought = investment / prices.iloc[0]
        cost = shares_bought * prices.iloc[0]

        end_value = shares_bought * prices.iloc[-1]

        stock_return = end_value - cost

        total_return += stock_return

    return total_return


total_return = backtest_investment_plan(investment_plan)

print(
    f"\nTotal return after 2 years: ${total_return:.2f}, which is a %{100 * (total_return/funds):.2f} return\n ")
