import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
from quote import quote

sns.set_style("dark")
sns.set_context("notebook")

def process_csv_files(csv_files, category):
    images_dir = f'static/images/{category}'
    os.makedirs(images_dir, exist_ok=True)

    for i, csv_file in enumerate(csv_files):
        data = pd.read_csv(f'data/{category}/{csv_file}')
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.sort_index(inplace=True)
        color = sns.color_palette("flare")[i % len(sns.color_palette("flare"))]
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor((236/255, 236/255, 244/255))
        ax.plot(data['close'], color=color, linewidth=2.0)
        ax.set_title(f'{csv_file[:-4]}')
        ax.grid(True)
        plt.savefig(os.path.join(images_dir, f'{csv_file[:-4]}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f'Saved {csv_file[:-4]}.png to {images_dir}')
        plt.close(fig)

categories = ['big_tech', 'misc', 'cancelled']

res = quote('Bill Gates')
print(f"\nDaily Bill Gates quote: {res[random.randint(0, len(res))]['quote']}\n")

for category in categories:
    
    csv_files = [f for f in os.listdir(f'data/{category}') if f.endswith('.csv')]
    process_csv_files(csv_files, category)

print("\n")