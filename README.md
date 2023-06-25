# Kingston Investment Tool

## Note: Currently in development. This version is not applicable to the average user (yet!). If you know what you're doing, then feel free to test it!

### This is an example of what the output currently looks like:

![example](https://raw.githubusercontent.com/gholtzap/kingston-invest/master/collage.png)

# Setup!
## Installing Stuffs:

### Automatic:
Type `.\setup.bat` in your terminal. This script should install everything necessary.
### Manual:
The libraries required are:
- requests
- tqdm
- python-dotenv
- randfacts
- quote
- pandas
- matplotlib
- seaborn
- Pillow
- Flask
- pyScss
- flask flask-wtf
- flask-assets

<br>

## API Key
#### For this project, I use the Alpha Vantage API. They currently offer free API keys. Head over [here](https://www.alphavantage.co/support/#api-key) to claim your free key.
Once you have your API key, create a file called `.env` inside the project's root directory.
Paste your API Key like this: `AV_API_KEY = "XXXXXXXXXXXXXXXXXX"`

Done!
<br>



# Using this Project
## Step 1: Generate your data
After everything has been installed and set up, type `.\update.bat` to run the project. This script will generate all data + images.
<br>

Bonus: if you would like to set this data as your wallpaper, then run `wallpaper.py`
<br>

## Step 2: Running the Webapp
After you have run `.\update.bat`, run `python app.py` to launch a local version of the webapp. Navigate to `locahost:5000` to see it.

