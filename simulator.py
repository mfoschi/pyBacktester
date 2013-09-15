#!/usr/bin/python

import csv
import json
from tester import Tester
from prices import PriceCandle, MAX_EMA_SIZE

__author__ = 'Marcello Foschi'


if __name__ == "__main__":
    config = json.load(open('config.json'))

    # build the history (list of candles)
    history = []
    INPUT_FILE = config['input_file']
    OUTPUT_FILE = config['output_file']
    with open(INPUT_FILE, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        last_candle = None
        for price in reader:
            new_candle = PriceCandle(int(price['Date']), float(price['Close']), last_candle)
            history.append(new_candle)
            last_candle = new_candle

    first_price = history[0].closing_value
    last_price = history[-1].closing_value
    bh_profit = 100*(last_price - first_price*(1+config['fees']/100)) / first_price
    print "Compare to B&H profit [%.2f to %.2f]: %.2f%%" % (first_price, last_price, bh_profit)

    if config['single_test']:
        backtest = Tester(config, history)
        backtest.print_results()
    else:
        with open(OUTPUT_FILE, 'wb') as csvfile:
            header_row = ['long_EMA']
            for index in range(1, MAX_EMA_SIZE):
                header_row.append(index)
            writer = csv.writer(csvfile)
            writer.writerow(header_row)
            for long_EMA in range(1, MAX_EMA_SIZE):
                config['long_EMA'] = long_EMA
                profit_row = [long_EMA]
                for short_EMA in range(1, long_EMA):
                    config['short_EMA'] = short_EMA
                    backtest = Tester(config, history)
                    profit = backtest.print_results()
                    profit_row.append(profit)
                writer.writerow(profit_row)
