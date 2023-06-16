import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style and context of seaborn
sns.set_style("dark")
sns.set_context("notebook")


################################################################################################
####################################### BIG TECH ###############################################
################################################################################################

# Get a list of all CSV files in the 'data' directory
big_tech_csv_files = [f for f in os.listdir('data/big_tech') if f.endswith('.csv')]
cancelled_csv_files = [f for f in os.listdir('data/cancelled') if f.endswith('.csv')]
misc_csv_files = [f for f in os.listdir('data/misc') if f.endswith('.csv')]

# Create images directory if it doesn't exist
images_dir = 'static/images/big-tech'
os.makedirs(images_dir, exist_ok=True)

for i, csv_file in enumerate(big_tech_csv_files):
    # Read the CSV data
    data = pd.read_csv(os.path.join('data/big_tech', csv_file))

    # Convert 'date' to datetime type
    data['date'] = pd.to_datetime(data['date'])

    # Set 'date' as the index of the dataframe
    data.set_index('date', inplace=True)

    # Sort the data by date (in case it's not sorted)
    data.sort_index(inplace=True)

    # Choose a color from seaborn's color palette
    color = sns.color_palette("flare")[i % len(sns.color_palette("flare"))]

    # Create a new figure for each CSV file
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set figure facecolor
    fig.patch.set_facecolor((236/255, 236/255, 244/255))
    
    # Plot data with increased line width
    ax.plot(data['close'], color=color, linewidth=2.0) 
    ax.set_title(f'{csv_file[:-4]}')
    ax.grid(True)

    # Save the figure to a file
    plt.savefig(os.path.join(images_dir, f'{csv_file[:-4]}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f'Saved {csv_file[:-4]}.png to {images_dir}')
    # Close the figure to free up memory
    plt.close(fig)


################################################################################################
####################################### Misc ###################################################
################################################################################################


# Get a list of all CSV files in the 'data' directory
misc_csv_files = [f for f in os.listdir('data/misc') if f.endswith('.csv')]

# Create images directory if it doesn't exist
images_dir = 'static/images/misc'
os.makedirs(images_dir, exist_ok=True)

for i, csv_file in enumerate(misc_csv_files):
    # Read the CSV data
    data = pd.read_csv(os.path.join('data/misc', csv_file))

    # Convert 'date' to datetime type
    data['date'] = pd.to_datetime(data['date'])

    # Set 'date' as the index of the dataframe
    data.set_index('date', inplace=True)

    # Sort the data by date (in case it's not sorted)
    data.sort_index(inplace=True)

    # Choose a color from seaborn's color palette
    color = sns.color_palette("flare")[i % len(sns.color_palette("flare"))]

    # Create a new figure for each CSV file
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set figure facecolor
    fig.patch.set_facecolor((236/255, 236/255, 244/255))
    
    # Plot data with increased line width
    ax.plot(data['close'], color=color, linewidth=2.0) 
    ax.set_title(f'{csv_file[:-4]}')
    ax.grid(True)

    # Save the figure to a file
    plt.savefig(os.path.join(images_dir, f'{csv_file[:-4]}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f'Saved {csv_file[:-4]}.png to {images_dir}')
    # Close the figure to free up memory
    plt.close(fig)


################################################################################################
####################################### Cancelled ##############################################
################################################################################################


# Get a list of all CSV files in the 'data' directory
cancelled_csv_files = [f for f in os.listdir('data/cancelled') if f.endswith('.csv')]

# Create images directory if it doesn't exist
images_dir = 'static/images/cancelled'
os.makedirs(images_dir, exist_ok=True)

for i, csv_file in enumerate(cancelled_csv_files):
    # Read the CSV data
    data = pd.read_csv(os.path.join('data/cancelled', csv_file))

    # Convert 'date' to datetime type
    data['date'] = pd.to_datetime(data['date'])

    # Set 'date' as the index of the dataframe
    data.set_index('date', inplace=True)

    # Sort the data by date (in case it's not sorted)
    data.sort_index(inplace=True)

    # Choose a color from seaborn's color palette
    color = sns.color_palette("flare")[i % len(sns.color_palette("flare"))]

    # Create a new figure for each CSV file
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set figure facecolor
    fig.patch.set_facecolor((236/255, 236/255, 244/255))
    
    # Plot data with increased line width
    ax.plot(data['close'], color=color, linewidth=2.0) 
    ax.set_title(f'{csv_file[:-4]}')
    ax.grid(True)

    # Save the figure to a file
    plt.savefig(os.path.join(images_dir, f'{csv_file[:-4]}.png'), bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f'Saved {csv_file[:-4]}.png to {images_dir}')
    # Close the figure to free up memory
    plt.close(fig)
