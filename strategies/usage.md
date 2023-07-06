**Strategies Usage**

1. Define amount of money in ``funds.json``
2. Define tickers in ``tickers.json``
3. Define which strategy you would like to use by changing the ``DESIRED_STRATEGY`` variable in ``invest.py``
4. Run ``invest.py``



**Purpose of each file:**
``generate_data.py`` : generates each stock's data for 4 *6-month intervals* & data for 2 years

*formula_stable.py* : formula for checking which tickers are the most stable

*invest.py*: takes the data and calculates the most efficient use of your money using the specified formula