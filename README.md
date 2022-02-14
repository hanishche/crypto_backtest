# crypto_backtest
Extracting crypto data from crypto compare and uploading it to MySQL DB. Using the data from MySQL DB, Backtest different models created using technical indicators like MACD,EMA,RSI and combinations of indicators.
While doing live trading it is possible that every crypto coin has different number of datapoints to look at, which can reduce the performance of indicators leading to more losses.
For example: For MANA coin at a give point of time from wazirx we might be having only last 2 hours of data instead of all 24 hours data(like data available for backtest).Hence i have created my own model which gonna compare the last 40 mins vs 150 mins vs 200 mins vs 300 mins at any given point of time for a coin. 
This repository consists of mainly 5 folders
1) USD  -- Contains Backtested data of Cryptos with USD currency
2) INR  -- Contains Backtested data of Cryptos with INR currency
3) Tableau files -- Tableau Dashboards
4) Indicators -- RSI,MACD, SToch RSI


6) Python scripts of models.![Crypto_flowchart](https://user-images.githubusercontent.com/32518059/153922122-270e09d5-285b-4132-b69e-505ab9ad1a9e.png)
