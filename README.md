# Kingston Investment Tool

## Note: Currently in development. This version is not applicable to the average user (yet!). If you know what you're doing, then feel free to test it!

# Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [API](#api)
4. [Strategies](#strategies)
5. [Index Maker](#index-maker)
6. [Timing](#timing)
7. [Collage](#collage)

# Versions
1. [V_1.0](#v_1_0)

## Introduction 
Hi! I'm getting into computational finance, and decided to create a repository full of miscellaneous tools that help me on the daily, so maybe they'll help you. I have a lot of docs on this project, so if you're confused just keep reading! The table of contents above lets you jump to all the different tools.

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
- yfinance
- shutil
- datetime

Here's a command to install all of the above at once:<br>
``pip install requests tqdm python-dotenv randfacts quote pandas matplotlib seaborn Pillow Flask pyScss flask-wtf flask-assets yfinance shutil``
<br>

### API Keys
- **PRE-REQUISITE: Create a file ``.env`` in the project's root directory. This is where your API keys will be stored.**
- Finnhub
    - I use the Finnhub API to retrieve financial data. [Get your free Finnhub API key here](https://finnhub.io/dashboard).
    - Once you have your Finnhub API key, add it to `.env` in the following format:
        - ``FINNHUB_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXX"``
        
        
- Alpha Vantage
    - I also use the Alpha Vantage API. They currently offer free API keys. Head over [here](https://www.alphavantage.co/support/#api-key) to claim your free key.
    - Once you have your API key, add it to `.env` in the following format:
        - `AV_API_KEY = "XXXXXXXXXXXXXXXXXX"`

Done!
<br>

## API

This is where I host Kingston's flask API.
<br>
Simply run ``python api/run.py`` to start the local server.
<br>
From there, you can connect to the API via normal HTTP requests.
<br>
Please note that you will need your own Finnhub API key stored in ``.env`` to return data. This API is not for public use yet.

### Endpoints:
- List of all endpoints and cURL / Javascript examples can be found in ``api/usage.md``
## Strategies
#### Description: <br>
Here you can run strategies that I have formulated throughout the years. They are named accordingly. 
 <br>

Instructions are found inside the strategies folder, read ``strategies/usage.md``.


#### Formulas, explained:
 A description of each formula and how it works can be found inside ``strategies/usage.md``.


## Index Maker
#### Description: <br>
Here you can create your own custom indices. Want to create the next SP500? Test it out here. <br>
Instructions are found inside the index-maker folder, read ``index-maker/usage.md``.

## Timing
Determines if it's the right time or not to buy stocks you're interested in, using the 2Q formula.<br>
Instructions are found inside the timing folder, read ``timing/usage.md``.

## Collage
#### Description: <br>
Generates a collage of all your favorite stocks and/or sets it as your desktop wallpaper.
![example](https://raw.githubusercontent.com/gholtzap/kingston-invest/master/collage.png)

#### Step 1 : Generate Your Data

Type `.\update.bat` to gather & download all data. This script will generate all data + images.
<br>

#### Step 2 : Run wallpaper.py
Run  ``wallpaper.py`` to set the collage as your wallpaper.




## V_1_0

### Date created : 7/20/2023
### Testing started : 7/21/2023

My first official version of my investing formulas! 

*More information can be found in ``V_1.0/usage.md``*
