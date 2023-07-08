# Kingston Investment Tool

## Note: Currently in development. This version is not applicable to the average user (yet!). If you know what you're doing, then feel free to test it!

# Table of Contents
1. [Introduction](#Introduction)
2. [Setup](#Setup)
3. [Webapp](#Webapp)
4. [Strategies](#Strategies)
5. [Index Maker](#index-maker)
6. [Collage](#Collage)

## Introduction 

## Setup
### Installing Libraries:
#### Automatic:
Type `.\setup.bat` in your terminal. This script should install everything necessary.
#### Manual:
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

Here's a command to install all of the above at once:<br>
``pip install requests tqdm python-dotenv randfacts quote pandas matplotlib seaborn Pillow Flask pyScss flask-wtf flask-assets``
<br>

### API Key
For this project, I use the Alpha Vantage API. They currently offer free API keys. Head over [here](https://www.alphavantage.co/support/#api-key) to claim your free key.
Once you have your API key, create a file called `.env` inside the project's root directory.
Paste your API Key like this: `AV_API_KEY = "XXXXXXXXXXXXXXXXXX"`

Done!
<br>

## Web App
After you have run `.\update.bat`, run `python app.py` to launch a local version of the webapp. Navigate to `locahost:5000` to see it.

## Strategies

## Index Maker

## Collage
#### Description: <br>
Generates a collage of all your favorite stocks and/or sets it as your desktop wallpaper.
![example](https://raw.githubusercontent.com/gholtzap/kingston-invest/master/collage.png)

Note: The below steps can be skipped by just running ``.\update.bat``. This script does all the steps automatically.

#### Step 1 : Generate Your Data

Type `.\update.bat` to gather & download all data. This script will generate all data + images.
<br>

#### Step 2 : Run wallpaper.py
Run ``collage.py`` then ``wallpaper.py`` to set the collage as your wallpaper.


