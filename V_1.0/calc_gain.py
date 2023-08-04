import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

with open('input/backtest.json', 'r') as f:
    data = json.load(f)

def calculate_gain(data, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    results = {}

    for category, stocks in data['Shares'].items():
        results[category] = {}

        initial_investment = 0
        final_value = 0

        for stock, shares in stocks.items():
            df = yf.download(stock, start=start_date_str, end=end_date_str)
            if not df.empty:
                cost = df.iloc[0]['Close'] * shares
                sales = df.iloc[-1]['Close'] * shares

                initial_investment += cost
                final_value += sales

                results[category][stock] = {
                    "start_price": df.iloc[0]['Close'],
                    "end_price": df.iloc[-1]['Close'],
                    "money_made": sales - cost
                }

        percentage_gain = (final_value - initial_investment) / initial_investment * 100

        results[category]['total'] = {
            "initial_investment": initial_investment,
            "final_value": final_value,
            "money_made": final_value - initial_investment,
            "percentage_gain_loss": percentage_gain
        }


    return results



def print_results(results):
    for category, stocks in results.items():
        print(f"\nCategory: {category}\n{'-'*50}")
        for stock, info in stocks.items():
            if stock == 'total':
                print(f"\nTotal:\n{'-'*50}")
                print(f"Initial Investment: ${info['initial_investment']:.2f}")
                print(f"Final Value: ${info['final_value']:.2f}")
                print(f"Money Made: ${info['money_made']:.2f}")
            else:
                print(f"\nStock: {stock}\n{'-'*50}")
                print(f"Start Price: ${info['start_price']:.2f}")
                print(f"End Price: ${info['end_price']:.2f}")
                print(f"Money Made: ${info['money_made']:.2f}")

def calculate_combined_results(results):
    combined_results = {
        "initial_investment": 0,
        "final_value": 0,
        "money_made": 0
    }

    for category, stocks in results.items():
        combined_results["initial_investment"] += stocks['total']["initial_investment"]
        combined_results["final_value"] += stocks['total']["final_value"]
        combined_results["money_made"] += stocks['total']["money_made"]

    combined_results["percentage_gain_loss"] = (combined_results["final_value"] - combined_results["initial_investment"]) / combined_results["initial_investment"] * 100

    return combined_results


plt.rcParams.update({'font.size': 20})


def plot_results(results, date_info):

    pastel_colors = ListedColormap(
        ['#FF6666', '#FFCC99', '#99FF99', '#66B3FF', '#c2c2f0', '#ffb3e6'])

    rows = 2
    cols = int(np.ceil((len(results) + 1) / 2))

    fig = plt.figure(figsize=(cols * 10, rows * 10))
    fig.suptitle(f'Collage for {date_info}', fontsize=30)

    plt.style.use('dark_background')

    overall_money_made = []

    for i, (category, stocks) in enumerate(results.items(), start=1):
        stocks = {k: v for k, v in stocks.items() if k != 'total'}

        labels = list(stocks.keys())
        money_made = [info['money_made'] for info in stocks.values()]

        overall_money_made.append(
            {'category': category, 'money_made': sum(money_made)})

        ax = fig.add_subplot(rows, cols, i)
        ax.barh(labels, money_made, color=pastel_colors.colors[:len(stocks)])

        ax.set_xlabel('Money Made')
        ax.set_title(f'Money Made by Each Stock in {category} Category')

    ax = fig.add_subplot(rows, cols, i + 1)
    labels = [item['category'] for item in overall_money_made]
    money_made = [item['money_made'] for item in overall_money_made]

    total_money = sum(money_made)
    money_made_percent = [(money / total_money) * 100 for money in money_made]

    ax.barh(labels, money_made_percent,
            color=pastel_colors.colors[:len(labels)])

    ax.set_xlabel('Total Money Made (%)')
    ax.set_title('Total Money Made by Category (Percentage)')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'collages/collage_{date_info.replace(" - ", "_")}.png')


with open('input/input_calc_gain.json', 'r') as f:
    dates = json.load(f)

combined_results = {
    "initial_investment": 0,
    "final_value": 0,
    "money_made": 0
}

for i, date_pair in enumerate(dates, start=1):
    result = calculate_gain(data, date_pair['start'], date_pair['end'])
    print_results(result)

    date_info = f"{date_pair['start']} - {date_pair['end']}"
    plot_results(result, date_info)
    
    # Add the results for this iteration to the combined totals
    total_for_iteration = calculate_combined_results(result)
    combined_results["initial_investment"] += total_for_iteration["initial_investment"]
    combined_results["final_value"] += total_for_iteration["final_value"]
    combined_results["money_made"] += total_for_iteration["money_made"]

combined_results["percentage_gain_loss"] = (combined_results["final_value"] - combined_results["initial_investment"]) / combined_results["initial_investment"] * 100

print("\n\nCombined Results:")
print(f"Initial Investment: ${combined_results['initial_investment']:.2f}")
print(f"Final Value: ${combined_results['final_value']:.2f}")
print(f"Money Made: ${combined_results['money_made']:.2f}")
print(f"Percentage Gain/Loss: {combined_results['percentage_gain_loss']:.2f}%")
