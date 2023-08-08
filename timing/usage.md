**TIMING**

How to use:

1. Delcare your desired tickers in ``tickers.json``
2. Run ``gen_data.py`` to generate data for those tickers
3. Run ``timing.py`` and/or ``sell.py``

The output will display which stocks you should or shouldn't buy from your list, ordered from best to worst.


Purpose of each file:

- gen_data.py: generates 4x 6 month intervals and 2 year time series data for each ticker
- timing.py: evaluates stocks according to the 2Q formula and determines if it is a buy or not
- sell.py: same thing as timing but reversed, tells if you should sell a stock or not


2Q formula:

- takes the average of each of the four six-month intervals. The second lowest average is the 'bar'. If a stock is below the bar, you buy it.