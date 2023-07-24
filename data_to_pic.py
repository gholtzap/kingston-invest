import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
import matplotlib.dates as mdates
from quote import quote

sns.set_context("notebook")


def process_csv_files(csv_files):
    images_dir = f'static/images/'
    os.makedirs(images_dir, exist_ok=True)

    for i, csv_file in enumerate(csv_files):
        data = pd.read_csv(f'data/stocks-12m/{csv_file}')
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.sort_index(inplace=True)

        with plt.style.context('dark_background'):
            color = sns.color_palette(
                "flare")[i % len(sns.color_palette("flare"))]
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data['close'], color=color, linewidth=2.0)
            ax.fill_between(data.index, data['close'], color=color, alpha=0.1)

            min_close = data['close'].min()
            max_close = data['close'].max()
            padding = (max_close - min_close) * 0.1
            ax.set_ylim([min_close - padding, max_close + padding])

            ax.set_title(
                f'{csv_file[:-4]} (Last 12 Months)', color='white', fontsize=30)
            ax.set_xlabel('Date', color='white')
            ax.set_ylabel('Closing Price', color='white')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.tick_params(colors='white')
            plt.savefig(os.path.join(
                images_dir, f'{csv_file[:-4]}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
            print(f'Saved {csv_file[:-4]}.png to {images_dir}')
            plt.close(fig)


csv_files = [f for f in os.listdir(f'data/stocks-12m/') if f.endswith('.csv')]
process_csv_files(csv_files)

print("\n")
