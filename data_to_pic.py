import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
import matplotlib.dates as mdates
from quote import quote
import json

sns.set_context("notebook")

def process_csv_files(csv_files):
    images_dir = 'static/images/'
    os.makedirs(images_dir, exist_ok=True)

    # Read the tickers and their buy details (if provided)
    with open('tickers.json') as f:
        tickers_data = json.load(f)
        buy_details = tickers_data['tickers']

    for i, csv_file in enumerate(csv_files):
        ticker = csv_file[:-4]  # Extract the ticker name from the filename
        data = pd.read_csv(f'data/stocks-12m/{csv_file}')
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.sort_index(inplace=True)

        with plt.style.context('dark_background'):
            color = sns.color_palette("flare")[i % len(sns.color_palette("flare"))]
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plotting the stock data
            ax.plot(data['close'], color=color, linewidth=2.0)
            ax.fill_between(data.index, data['close'], color=color, alpha=0.1)

            # If a buy_price is provided for the ticker, draw the horizontal line
            if ticker in buy_details and "buy_price" in buy_details[ticker]:
                ax.axhline(buy_details[ticker]["buy_price"], color='red', linestyle='--', linewidth=3, label="Buy Price")
                
            # If a buy_date is provided for the ticker, draw the vertical line
            if ticker in buy_details and "buy_price" in buy_details[ticker]:
                buy_price = buy_details[ticker]["buy_price"]
                ax.axhline(buy_price, color='gold', linestyle='--', linewidth=3, label="Buy Price")
                
                # Get the date with the closest closing price to the buy_price
                closest_date = data.iloc[(data['close'] - buy_price).abs().argsort()[:1]].index[0]
                
                ax.axvline(closest_date, color='teal', linestyle='--', linewidth=3, label="Buy Date")
                ax.legend(loc="upper left", fontsize=10, facecolor="black")


            # Setting other graph details
            min_close = data['close'].min()
            max_close = data['close'].max()
            padding = (max_close - min_close) * 0.1
            ax.set_ylim([min_close - padding, max_close + padding])

            ax.set_title(f'{ticker} (Last 12 Months)', color='white', fontsize=30)
            ax.set_xlabel('Date', color='white')
            ax.set_ylabel('Closing Price', color='white')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.tick_params(colors='white')
            
            # Saving the plot
            plt.savefig(os.path.join(images_dir, f'{ticker}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
            print(f'Saved {ticker}.png to {images_dir}')
            
            plt.close(fig)



def remove_unwanted_images():
    images_dir = 'static/images/'

    with open('tickers.json') as f:
        tickers_data = json.load(f)
        tickers = list(tickers_data['tickers'].keys())
        buy_prices = tickers_data['tickers']


    for filename in os.listdir(images_dir):
        ticker_filename = os.path.splitext(filename)[0]
        if ticker_filename not in tickers:
            os.remove(os.path.join(images_dir, filename))
            print(f"Deleted image for {ticker_filename} as it does not exist in tickers.json")

csv_files = [f for f in os.listdir(f'data/stocks-12m/') if f.endswith('.csv')]
process_csv_files(csv_files)
remove_unwanted_images() 
print("\n")