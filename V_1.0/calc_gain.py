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
    # Parse the start and end dates
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    results = {}

    for category, stocks in data['Shares'].items():
        results[category] = {}

        # Assume you start with $0
        initial_investment = 0
        final_value = 0

        for stock, shares in stocks.items():
            # Get stock historical data from the Yahoo Finance
            df = yf.download(stock, start=start_date_str, end=end_date_str)
            if not df.empty:
                # Calculate the cost and the sales
                cost = df.iloc[0]['Close'] * shares
                sales = df.iloc[-1]['Close'] * shares

                # Update the initial investment and final value
                initial_investment += cost
                final_value += sales

                # Store the start and end prices, and the money made
                results[category][stock] = {
                    "start_price": df.iloc[0]['Close'],
                    "end_price": df.iloc[-1]['Close'],
                    "money_made": sales - cost
                }

        # Store the total initial investment and final value for the category
        results[category]['total'] = {
            "initial_investment": initial_investment,
            "final_value": final_value,
            "money_made": final_value - initial_investment
        }

    return results

# Example usage:
#print(calculate_gain(data, '2022-07-21', '2023-05-28'))


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

# Then use print_results function in your script like this

#result = calculate_gain(data, '2023-07-12', '2023-07-20')
#print_results(result)

plt.rcParams.update({'font.size': 20})

def plot_results(results, date_info):
    
    # Prepare pastel colormap
    pastel_colors = ListedColormap(['#FF6666', '#FFCC99', '#99FF99', '#66B3FF', '#c2c2f0', '#ffb3e6'])

    # Define the number of rows and columns for the subplot grid
    rows = 2
    cols = int(np.ceil((len(results) + 1) / 2))  # Add 1 for the 'Overall' category

    # Create a new figure with a size based on the number of rows
    fig = plt.figure(figsize=(cols * 10, rows * 10))
    fig.suptitle(f'Collage for {date_info}', fontsize=30)

    # Set the dark background style
    plt.style.use('dark_background')

    # Prepare the data for the 'Overall' category
    overall_money_made = []

    for i, (category, stocks) in enumerate(results.items(), start=1):
        # Remove the 'total' entry for the plot
        stocks = {k: v for k, v in stocks.items() if k != 'total'}

        # Prepare the data for the plot
        labels = list(stocks.keys())
        money_made = [info['money_made'] for info in stocks.values()]

        # Append the money made in this category to the overall money made
        overall_money_made.append({'category': category, 'money_made': sum(money_made)})

        # Create the subplot
        ax = fig.add_subplot(rows, cols, i)
        ax.barh(labels, money_made, color=pastel_colors.colors[:len(stocks)])

        # Set the title and labels
        ax.set_xlabel('Money Made')
        ax.set_title(f'Money Made by Each Stock in {category} Category')

    # Create the 'Overall' subplot
    ax = fig.add_subplot(rows, cols, i + 1)
    labels = [item['category'] for item in overall_money_made]
    money_made = [item['money_made'] for item in overall_money_made]
    
    # Convert total money made into percentage
    total_money = sum(money_made)
    money_made_percent = [(money / total_money) * 100 for money in money_made]

    ax.barh(labels, money_made_percent, color=pastel_colors.colors[:len(labels)])

    ax.set_xlabel('Total Money Made (%)')
    ax.set_title('Total Money Made by Category (Percentage)')

    # Save the plot as an image
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave some space at the top for the suptitle
    plt.savefig(f'collages/collage_{date_info.replace(" - ", "_")}.png')

#plot_results(result)


# Load dates from JSON file
with open('input/input_calc_gain.json', 'r') as f:
    dates = json.load(f)

# For each pair of dates in the list
for i, date_pair in enumerate(dates, start=1):
    # Calculate results
    result = calculate_gain(data, date_pair['start'], date_pair['end'])
    print_results(result)

    # Plot results
    date_info = f"{date_pair['start']} - {date_pair['end']}"
    plot_results(result, date_info)

    # Save the plot as an image with a unique name
    #plt.tight_layout()
    #plt.savefig(f'collages/calc_gain/collage_{i}.png')