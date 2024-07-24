import os
import pandas as pd
import json
from termcolor import colored

def load_parameters(file_path):
    with open(file_path, 'r') as file:
        params = json.load(file)
        # Convert percentage strings to numerical values
        params['dip_percentage_min'] = 1 - float(params['dip_percentage_min'].strip('%')) / 100
        params['dip_percentage_max'] = 1 - float(params['dip_percentage_max'].strip('%')) / 100
        params['rise_percentage'] = 1 + float(params['rise_percentage'].strip('%')) / 100
        return params

def run_strategy_on_combined_data(combined_data, parameters):
    buys = []
    sells = []
    holdings = {}
    initial_capital = parameters['initial_capital']
    capital = initial_capital
    earnings = 0.0
    total_profit = 0.0
    trading_days = 0

    for i in range(1, len(combined_data)):
        row = combined_data.iloc[i]
        previous_row = combined_data.iloc[i - 1]
        previous_close = previous_row['close']
        current_close = row['close']
        stock = row['stock']
        date = row['date']

        if stock not in holdings:
            holdings[stock] = {'holding': False, 'buy_price': 0.0, 'shares_held': 0.0}

        # Recalculate position size based on current capital
        position_size = parameters['position_size_ratio'] * capital

        # Buy condition: dips within the specified range from previous close
        if not holdings[stock]['holding'] and previous_close * parameters['dip_percentage_max'] <= current_close <= previous_close * parameters['dip_percentage_min']:
            total_value = position_size
            buys.append((date, stock, current_close, total_value, capital))
            holdings[stock]['holding'] = True
            holdings[stock]['buy_price'] = current_close
            holdings[stock]['shares_held'] = position_size / current_close
            capital -= position_size

        # Sell condition: increases by the specified percentage from buy price
        if holdings[stock]['holding'] and current_close >= holdings[stock]['buy_price'] * parameters['rise_percentage']:
            profit = holdings[stock]['shares_held'] * (current_close - holdings[stock]['buy_price'])
            total_value = holdings[stock]['shares_held'] * current_close
            sells.append((date, stock, current_close, holdings[stock]['buy_price'], profit, total_value, capital))
            holdings[stock]['holding'] = False
            capital += holdings[stock]['shares_held'] * holdings[stock]['buy_price']  # only add the initial investment back to capital
            earnings += profit  # add the profit to the earnings pile
            holdings[stock]['shares_held'] = 0.0
            total_profit += profit
        trading_days += 1

    # Final capital after all transactions, excluding any open trades
    total_returns = earnings
    avg_profit_per_day = total_profit / trading_days if trading_days > 0 else 0
    avg_percentage_per_day = (avg_profit_per_day / initial_capital) * 100

    return buys, sells, total_returns, avg_profit_per_day, avg_percentage_per_day

def get_color(profit):
    if profit > 0:
        return 'green'
    elif profit < 0:
        return 'red'
    else:
        return 'white'

def process_all_files(directory, parameters):
    combined_data = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            stock_data = pd.read_csv(file_path)
            stock_data['stock'] = os.path.splitext(filename)[0]
            combined_data.append(stock_data)
    
    combined_data = pd.concat(combined_data)
    combined_data['date'] = pd.to_datetime(combined_data['date'])
    combined_data.sort_values(by=['date', 'stock'], inplace=True)
    combined_data.reset_index(drop=True, inplace=True)

    buys, sells, total_returns, avg_profit_per_day, avg_percentage_per_day = run_strategy_on_combined_data(combined_data, parameters)

    print(colored("Buys:", 'blue'))
    for buy in buys:
        print(colored("Date: {}, Stock: {}, Price: ${:.2f}, Total Value: ${:.2f}, Capital After Trade: ${:.2f}".format(buy[0], buy[1], buy[2], buy[3], buy[4]), 'blue'))
    print("\n" + colored("Sells:", 'magenta'))
    for sell in sells:
        profit = sell[4]
        color = get_color(profit)
        print(colored("Date: {}, Stock: {}, Sell Price: ${:.2f}, Buy Price: ${:.2f}, Profit: ${:.2f}, Total Value: ${:.2f}, Capital After Trade: ${:.2f}".format(sell[0], sell[1], sell[2], sell[3], profit, sell[5], sell[6]), color))
    print("\n" + colored("Total Returns: ${:.2f}".format(total_returns), 'cyan'))
    print(colored("Average Money Made Per Day: ${:.2f}".format(avg_profit_per_day), 'cyan'))
    print(colored("Average Percentage of Initial Investment Made Per Day: {:.4f}%".format(avg_percentage_per_day), 'cyan'))

if __name__ == "__main__":
    parameters = load_parameters("strat.json")
    directory = parameters['data_directory']
    process_all_files(directory, parameters)
