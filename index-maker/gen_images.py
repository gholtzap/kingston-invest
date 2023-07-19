import matplotlib.pyplot as plt
import json
import pandas as pd
import yfinance as yf
import os
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        ticker_data = yf.download(ticker, start=start_date, end=end_date)
        data[ticker] = ticker_data["Adj Close"]
    return pd.DataFrame(data)

def create_index(df):
    return df.sum(axis=1)

pastel_colors = [
    "#ffb3ba", "#ffdfba", "#ffffba", "#baffc9", "#bae1ff",
    "#AEC6CF", "#F778A1", "#E2F0CB", "#FF6961", "#CB99C9",
    "#DEA5A4", "#B39EB5", "#FFB347", "#FAE7B5", "#D1E231",
    "#AEC6CF", "#F778A1", "#E2F0CB", "#FF6961", "#CB99C9",
]

index_color = "#FFB3BA"  # pastel red
comparison_ticker_colors = {
    "^GSPC": "#FFFFBA",  # pastel yellow
    "^DJI": "#FFDFBA",  # pastel orange
}

def process_indices(start_date, end_date, category, comparison_tickers=["^GSPC", "^DJI"]):
    images_dir = f'static/images/{category}'
    os.makedirs(images_dir, exist_ok=True)
    
    comparison_data = get_data(comparison_tickers, start_date, end_date)
    
    
    with open("indices.json") as f:
        indices = json.load(f)
        
    all_tickers = [ticker for sublist in indices.values() for ticker in sublist]
    ticker_color_map = {ticker: color for ticker, color in zip(all_tickers, pastel_colors)}
    
    
    for index_name, tickers in indices.items():
        data = get_data(tickers, start_date, end_date)
        index = create_index(data)

        last_prices = data.iloc[-1]
        total = last_prices.sum()
        contributions = last_prices / total * 100 

        with plt.style.context('dark_background'):  
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
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) 
            ax.tick_params(colors='white') 

            contributions_sorted = contributions.sort_values(ascending=False)
            legend_text = "\n".join([f"{ticker}: {contributions_sorted[ticker]:.2f}%" for ticker in contributions_sorted.index])
            ax.text(1.02, 0.5, legend_text, transform=ax.transAxes, fontsize=10, verticalalignment='center')

            ax.legend([index_name] + comparison_tickers, loc='upper left')

            plt.savefig(os.path.join(images_dir, f'{index_name}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
            print(f'Saved {index_name}.png to {images_dir}')
            plt.close(fig)




process_indices("2020-01-01", "2023-12-31", "custom_indices")
