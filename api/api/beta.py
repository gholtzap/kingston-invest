import io
import json
import os
from flask import send_file, Response

from matplotlib import dates, pyplot as plt
import pandas as pd
import yfinance


def get_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        ticker_data = yfinance.download(ticker, start=start_date, end=end_date)
        data[ticker] = ticker_data["Adj Close"]
    return pd.DataFrame(data)

def create_index(df):
    return df.sum(axis=1)

def generate_index_and_image(data):
    
    index_color = "#FFB3BA"  # pastel red
    comparison_ticker_colors = {
        "^GSPC": "#FFFFBA",  # pastel yellow
        "^DJI": "#FFDFBA",  # pastel orange
    }
    index_name = data['index_name']
    tickers = data['tickers']

    start_date = "2020-01-01"  # these can also be input by user if you like
    end_date = "2023-12-31"
    comparison_tickers=["^GSPC", "^DJI"]

    # Get ticker data and create index
    data = get_data(tickers, start_date, end_date)
    index = create_index(data)

    comparison_data = get_data(comparison_tickers, start_date, end_date)
    
    # Generate image
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(index, color=index_color, linewidth=1.0, label=index_name) 
    ax.fill_between(index.index, index, color=index_color, alpha=0.1)
    for ticker in comparison_tickers:
        color = comparison_ticker_colors.get(ticker, "black") 
        ax.plot(comparison_data[ticker] * (index[0] / comparison_data[ticker][0]), label=ticker, color=color, linewidth=1.0)
    min_close = index.min()
    max_close = index.max()
    padding = (max_close - min_close) * 0.1
    ax.set_ylim([min_close - padding, max_close + padding])
    ax.set_title(f'{index_name}', color='white', fontsize=30) 
    ax.set_xlabel('Date', color='white')  
    ax.set_ylabel('Index Value', color='white') 
    ax.grid(True, linewidth=0.5, color='#d3d3d3', linestyle='-') 
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b %Y')) 
    ax.tick_params(colors='white') 
    last_prices = data.iloc[-1]
    total = last_prices.sum()
    contributions = last_prices / total * 100 
    contributions_sorted = contributions.sort_values(ascending=False)
    legend_text = "\n".join([f"{ticker}: {contributions_sorted[ticker]:.2f}%" for ticker in contributions_sorted.index])
    ax.text(1.02, 0.5, legend_text, transform=ax.transAxes, fontsize=10, verticalalignment='center')
    ax.legend([index_name] + comparison_tickers, loc='upper left')

    # Save the figure to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    plt.close(fig)
    image_stream.seek(0)  # rewind the file pointer to the beginning of the BytesIO object

    # Create a Flask response
    response = Response(image_stream, mimetype='image/png')
    response.headers["Content-Disposition"] = "attachment; filename=index_plot.png"
    
    return response