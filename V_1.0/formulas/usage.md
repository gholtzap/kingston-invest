**Formulas Usage**

1. Run ``test.sh`` (be patient, it takes a minute!)
2. View results in ``output.json``

**Description of each Strategy**

1. **nike.py**
- Based on linear regression analysis. Stocks are selected if the slope of their price trend has been negative in the past seven days but is positive in the most recent observation. The selected stocks are then allocated equal funds.
- It is called 'nike' as the ideal 8-day stock graph for this formula will look like a check mark. Note that this formula is very selective and might not return any stocks if it doesn't fit the criteria.

2. **ma.py**
- Moving-average. Selects stocks if their 50-day moving average is higher than their 200-day moving average. The allocation of funds is based on the golden ratio.

3. **macd.py**
- Moving Average Convergence Divergence (MACD) strategy. calculates the MACD line and signal line using exponential moving averages (EMAs) based on specified window lengths. Stocks are selected if the MACD line is above the signal line and if the previous MACD value was below the previous signal value. Funds are allocated equally among the selected stocks.

4. **rsi.py**
- Relative Strength Index (RSI) strategy for stock investment. It calculates the RSI indicator based on the closing prices and a specified time window. Stocks are selected if their RSI value is below 30 and if the previous RSI value was above 30. Funds are allocated equally among the selected stocks.

5. **iman.py**
- Based on a score calculation using volatility and moving averages. It calculates the score for each stock based on the volatility of the price changes over the last 30 days. Stocks with higher scores are considered more desirable. The top-performing stocks based on their scores are selected, and funds are allocated equally among them.

6. **rk2.py**
- Based on the Price-to-Earnings (P/E) ratio and EPS (Earnings Per Share) data. Calculates the P/E ratio for each stock. Stocks are selected based on the lowest P/E ratios. 

7. **diwi.py**
- Calculates the number of "hard dips" for each stock, where a hard dip is defined as the stock's closing price falling below 80% of its 30-day simple moving average (SMA). The top-performing stocks with the highest total number of hard dips are selected.
