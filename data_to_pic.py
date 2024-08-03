import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
import coloredlogs
import json
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

coloredlogs.install(level='INFO')
logging.basicConfig(level='INFO')

sns.set_context("notebook")

def process_csv_files(months=12):
    images_dir = 'static/images/'
    csv_files = [f for f in os.listdir(f'data/amun/stocks-{months}m/') if f.endswith('.csv')]
    os.makedirs(images_dir, exist_ok=True)

    with open('tickers_amun.json') as f:
        tickers_data = json.load(f)
        buy_details = tickers_data['tickers']

    highlighted_stocks = {"cyan": [], "orange": [], "magenta": []}
    stock_performance = {}
    highlighted_stocks_data = {}

    for i, csv_file in enumerate(csv_files):
        ticker = csv_file[:-4]  # Extract the ticker name from the filename
        
        data = pd.read_csv(f'data/amun/stocks-{months}m/{csv_file}')
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.sort_index(inplace=True)
        
        # Calculate the rolling 7-day minimum price
        data['rolling_7d_min'] = data['close'].rolling(window=7).min()

        # Check if the current day's price is less than 90% of the price from 7 days ago
        data['highlight'] = data['close'] < 0.9 * data['rolling_7d_min'].shift(7)

        latest_price = data['close'].iloc[-1]
        buy_price = buy_details.get(ticker, {}).get('buy_price', None)
        buy_date = pd.to_datetime(buy_details.get(ticker, {}).get('buy_date', ''), errors='coerce')

        # Initialize magenta and cyan dates and prices for each ticker
        if ticker not in highlighted_stocks_data:
            highlighted_stocks_data[ticker] = {'magenta_dates': [], 'magenta_prices': [], 'cyan_dates': [], 'cyan_prices': []}

        # Check for magenta highlight throughout the data
        for idx, row in data.iterrows():
            if row['highlight']:
                highlighted_stocks_data[ticker]['magenta_dates'].append(idx.strftime('%Y-%m-%d'))
                highlighted_stocks_data[ticker]['magenta_prices'].append(row['close'])
                if idx == data.index[-1]:
                    highlighted_stocks['magenta'].append(ticker)

        # Check if the latest price has increased 30% from the buy price
        if buy_price and latest_price >= 1.3 * buy_price:
            highlighted_stocks['orange'].append(ticker)

        if ticker in buy_details:
            stock_performance[ticker] = calculate_performance(data, buy_date, buy_price)

        with plt.style.context('dark_background'):
            color = sns.color_palette("flare")[i % len(sns.color_palette("flare"))]
            fig, ax = plt.subplots(figsize=(11, 7))
            
            for idx, row in data.iterrows():
                if row['highlight']:
                    ax.axvspan(idx - pd.Timedelta(days=1), idx + pd.Timedelta(days=1), color='magenta', alpha=0.3)
    
            border_color = "none"
            
            if data['highlight'].iloc[-1] and (ticker in buy_details and "buy_price" in buy_details[ticker]):
                for spine in ax.spines.values():
                    spine.set_linewidth(2)
                    spine.set_edgecolor('cyan')
                border_color = "cyan"
                highlighted_stocks["cyan"].append(ticker)
            elif ticker in buy_details and "buy_price" in buy_details[ticker]:
                for spine in ax.spines.values():
                    spine.set_linewidth(2)
                    spine.set_edgecolor('orange')
                border_color = "orange"
            elif data['highlight'].iloc[-1]:
                for spine in ax.spines.values():
                    spine.set_linewidth(2)
                    spine.set_edgecolor('magenta')
                border_color = "magenta"

            # Plotting the stock data
            ax.plot(data['close'], color=color, linewidth=2.0)
            ax.fill_between(data.index, data['close'], color=color, alpha=0.1)

            if ticker in buy_details and "buy_price" in buy_details[ticker]:
                ax.axhline(buy_details[ticker]["buy_price"], color='orange', linestyle='--', linewidth=3)

            if ticker in buy_details and "buy_date" in buy_details[ticker]:
                try:
                    buy_date = pd.to_datetime(buy_details[ticker]["buy_date"])
                    ax.axvline(buy_date, color='teal', linestyle='--', linewidth=3)
                except ValueError:
                    logging.error(f"Invalid date format for ticker {ticker}: {buy_details[ticker]['buy_date']}")

            # Check for cyan highlight based on magenta price increase by 30%
            for magenta_date_str, magenta_price in zip(highlighted_stocks_data[ticker]['magenta_dates'], highlighted_stocks_data[ticker]['magenta_prices']):
                magenta_date = pd.to_datetime(magenta_date_str)
                future_data = data.loc[magenta_date:]
                for future_idx, future_row in future_data.iterrows():
                    if future_row['close'] >= 1.3 * magenta_price:
                        highlighted_stocks_data[ticker]['cyan_dates'].append(future_idx.strftime('%Y-%m-%d'))
                        highlighted_stocks_data[ticker]['cyan_prices'].append(future_row['close'])
                        ax.axvline(future_idx, color='cyan', linestyle='-', linewidth=3)
                        break

            min_close = data['close'].min()
            max_close = data['close'].max()
            padding = (max_close - min_close) * 0.1
            ax.set_ylim([min_close - padding, max_close + padding])

            ax.set_title(f'{ticker} | 1y', color='white', fontsize=30)
            ax.set_xlabel('Date', color='white')
            ax.set_ylabel('Closing Price', color='white')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.tick_params(colors='white')

            modified_filename = f"{ticker}_{border_color}_{months}.png"
            existing_files = [f for f in os.listdir(images_dir) if f.startswith(f"{ticker}_") and f != modified_filename]
            for existing_file in existing_files:
                os.remove(os.path.join(images_dir, existing_file))
                logging.info(f"Removed outdated file: {existing_file}")

            logging.info(f'Saved {modified_filename} to {images_dir}')
            
            plt.tight_layout()
            plt.savefig(os.path.join(images_dir, modified_filename), dpi=100)
            plt.close(fig)

    # Export highlighted stocks and performance data to a JSON file
    with open('highlighted_stocks.json', 'w') as json_file:
        json.dump({'highlighted_stocks': highlighted_stocks, 'stock_performance': stock_performance, 'highlighted_stocks_data': highlighted_stocks_data}, json_file)

    return highlighted_stocks

def calculate_performance(data, buy_date, buy_price):
    performance = {}
    today = data.index[-1]

    # Calculate 1d, 5d, 1mo, 6mo, 12mo performance
    performance['1d'] = calculate_return(data, data.index[-2], today)
    performance['5d'] = calculate_return(data, get_trading_date(data, today, -5), today)
    performance['1mo'] = calculate_return(data, get_trading_date(data, today, -21), today)  # Approx 21 trading days in a month
    performance['6mo'] = calculate_return(data, get_trading_date(data, today, -126), today)  # Approx 126 trading days in 6 months
    performance['12mo'] = calculate_return(data, get_trading_date(data, today, -252), today)  # Approx 252 trading days in a year

    # Calculate performance since purchase
    if pd.notnull(buy_date) and buy_date in data.index:
        performance['since_buy'] = calculate_return(data, buy_date, today)
    elif buy_price is not None:
        start_price = buy_price
        end_price = data['close'].iloc[-1]
        performance['since_buy'] = f"{((end_price - start_price) / start_price) * 100:.2f}%"
    else:
        performance['since_buy'] = 'n/a'
    
    logging.info(f"Performance for {data.index[-1]}: {performance}")
    return performance

def get_trading_date(data, end_date, offset):
    # Adjust the end_date to account for non-trading days
    trading_dates = data.index
    try:
        position = trading_dates.get_loc(end_date)
    except KeyError:
        position = trading_dates.get_loc(end_date, method='pad')
    new_position = position + offset
    if new_position < 0:
        return trading_dates[0]
    elif new_position >= len(trading_dates):
        return None
    return trading_dates[new_position]

def calculate_return(data, start_date, end_date):
    if start_date is None or end_date is None:
        return 'n/a'
    start_price = data.loc[start_date]['close']
    end_price = data.loc[end_date]['close']
    return f"{((end_price - start_price) / start_price) * 100:.2f}%"

def remove_unwanted_images():
    images_dir = 'static/images/'

    with open('tickers_amun.json') as f:
        tickers_data = json.load(f)
        tickers = list(tickers_data['tickers'].keys())

    for filename in os.listdir(images_dir):
        ticker_from_filename = filename.split('_')[0]
        
        if ticker_from_filename not in tickers:
            os.remove(os.path.join(images_dir, filename))
            logging.info(f"Deleted image for {ticker_from_filename} as it does not exist in tickers_amun.json")

# Process CSV files and remove unwanted images
process_csv_files()
remove_unwanted_images()
