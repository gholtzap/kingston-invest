import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
import matplotlib.dates as mdates
from quote import quote

sns.set_context("notebook")

def process_csv_files(csv_files, category):
    images_dir = f'static/images/{category}'
    os.makedirs(images_dir, exist_ok=True)

    for i, csv_file in enumerate(csv_files):
        data = pd.read_csv(f'data/{category}/{csv_file}')
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.sort_index(inplace=True)
        
        with plt.style.context('dark_background'):  
            color = sns.color_palette("flare")[i % len(sns.color_palette("flare"))] 
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data['close'], color=color, linewidth=2.0) 
            ax.fill_between(data.index, data['close'], color=color, alpha=0.1) 
            ax.set_title(f'{csv_file[:-4]} (Last 6 Months)', color='white',fontsize=30) 
            ax.set_xlabel('Date', color='white')  
            ax.set_ylabel('Closing Price', color='white') 
            ax.grid(True, linewidth=0.5, color='#d3d3d3', linestyle='-') 
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) 
            ax.tick_params(colors='white') 
            plt.savefig(os.path.join(images_dir, f'{csv_file[:-4]}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
            print(f'Saved {csv_file[:-4]}.png to {images_dir}')
            plt.close(fig)

categories = ['big_tech', 'misc', 'cancelled']

res = quote('Bill Gates')

try:
    print(f"\nDaily Bill Gates quote: {res[random.randint(0, len(res))]['quote']}\n")
except IndexError:
    print("\nNo quotes from Bill Gates available today.\n")

for category in categories:
    csv_files = [f for f in os.listdir(f'data/{category}') if f.endswith('.csv')]
    process_csv_files(csv_files, category)

print("\n")
