## Python Bitcoin Backtester ##

### Overview ###

Python script to backtest EMA crossing.
Still in very early stage of development.

### Usage ###

* Download historic values to candles.csv (can reuse candles from gekko-backtester)
* Edit the parameters in config.json (JSON format)
* run simulator.py
* To create a matrix of performance for a range of parameters: set single_test to false, and specify the output_file.

### Future features ###

* Fetch data from different exchanges.
* Live monitoring of price changes.
