
**Strategies Usage**

1. Run ``test.sh`` (be patient, it takes a minute!)
2. View results in ``formulas/output.json``


**Description of each Strategy**


1. **ma.py**
- Moving-average. Selects stocks if their 50-day moving average is higher than their 200-day moving average. The allocation of funds is based on the golden ratio.

2. **macd.py**
- Moving Average Convergence Divergence (MACD) strategy. calculates the MACD line and signal line using exponential moving averages (EMAs) based on specified window lengths. Stocks are selected if the MACD line is above the signal line and if the previous MACD value was below the previous signal value. Funds are allocated equally among the selected stocks.

3. **rsi.py**
- Relative Strength Index (RSI) strategy for stock investment. It calculates the RSI indicator based on the closing prices and a specified time window. Stocks are selected if their RSI value is below 30 and if the previous RSI value was above 30. Funds are allocated equally among the selected stocks.

4. **iman.py**
- Based on a score calculation using volatility and moving averages. It calculates the score for each stock based on the volatility of the price changes over the last 30 days. Stocks with higher scores are considered more desirable. The top-performing stocks based on their scores are selected, and funds are allocated equally among them.

5. **diwi.py**
- Calculates the number of "hard dips" for each stock, where a hard dip is defined as the stock's closing price falling below 80% of its 30-day simple moving average (SMA). The top-performing stocks with the highest total number of hard dips are selected.




**Patch Notes**

1. All formulas now only select 6 stocks instead of 10
2. All formulas now allocate funds according to these proportions:
    - ``0.38 0.26 0.12 0.08 0.08 0.08``
3. Nike formula removed
4. RK formula removed


