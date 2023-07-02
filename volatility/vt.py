import os
import requests
import numpy as np
from dotenv import load_dotenv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

load_dotenv()

def calculate_vt(symbol):
    API_KEY = os.getenv('AV_API_KEY')

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    print(data)
    close_prices = [float(values['5. adjusted close']) for values in data['Time Series (Daily)'].values()]

    daily_returns = [0]
    for i in range(1, len(close_prices)):
        daily_returns.append((close_prices[i] - close_prices[i-1]) / close_prices[i-1])

    volatility = np.std(daily_returns) * np.sqrt(252) 

    return volatility

def calculate_vt_and_graph(symbol, data):
    dates = [pd.to_datetime(date) for date in data['Time Series (Daily)'].keys()]
    close_prices = [float(values['5. adjusted close']) for values in data['Time Series (Daily)'].values()]

    df = pd.DataFrame({
        'date': dates,
        'close': close_prices
    })

    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    daily_returns = df['close'].pct_change().dropna()

    volatility = daily_returns.std() * (252**0.5) 

    with plt.style.context('dark_background'):  
        color = sns.color_palette("flare")[0] 
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['close'], color=color, linewidth=2.0) 
        ax.fill_between(df.index, df['close'], color=color, alpha=0.1)
        
        min_close = df['close'].min()
        max_close = df['close'].max()
        padding = (max_close - min_close) * 0.1
        ax.set_ylim([min_close - padding, max_close + padding])
        
        ax.set_title(f'{symbol.upper()} (Last 6 Months)', color='white', fontsize=30) 
        ax.set_xlabel('Date', color='white')  
        ax.set_ylabel('Closing Price', color='white') 
        ax.grid(True, linewidth=0.5, color='#d3d3d3', linestyle='-') 
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) 
        ax.tick_params(colors='white') 

        images_dir = 'static/images'
        os.makedirs(images_dir, exist_ok=True)
        plt.savefig(os.path.join(images_dir, f'{symbol}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f'Saved {symbol}.png to {images_dir}')
        plt.close(fig)

    return volatility

def get_data(symbol):
    API_KEY = os.getenv('AV_API_KEY')
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    return data

if __name__ == "__main__":
    symbol = input("Enter a ticker symbol: ")
    volatility = calculate_vt(symbol)
    print(f"The annualized volatility for {symbol} is {volatility}")
