from prices import Indicator

__author__ = 'Marcello Foschi'


class Tester():
    current_trend = None
    trades_number = 0

    def get_last(self):
        if len(self.indicators) == 0:
            return None
        else:
            return self.indicators[-1].candle

    def add_candle(self, candle):
        indicator = Indicator(self, candle)
        operation = indicator.advice
        if operation is not None:
            self.trades_number += 1
            price = candle.closing_value
            if (operation == "BUY") & (self.usdAccount > 0):
                self.usdAccount *= (1 - self.fees/100)
                self.btcAccount = self.usdAccount / price
                self.usdAccount = 0
            if (operation == "SELL") & (self.btcAccount > 0):
                self.usdAccount = self.btcAccount * price
                self.usdAccount *= (1 - self.fees/100)
                self.btcAccount = 0
        self.indicators.append(indicator)

    def print_results(self):
        print "%s trades, end value: %.3f BTC and %.2f USD" % (self.trades_number, self.btcAccount, self.usdAccount)
        if self.btcAccount > 0:
            last_value = self.get_last().closing_value
            print "Sell all BTC at %s to calculate profit" % last_value
            self.usdAccount += self.btcAccount * last_value
            self.btcAccount = 0
        profit = 100*(self.usdAccount - self.starting_USD) / self.starting_USD
        print "EMA %s/%s total profit USD: %.2f%%" % (self.short_EMA, self.long_EMA, profit)
        return profit

    def __init__(self, config, history):
        self.short_EMA = config['short_EMA']
        self.long_EMA = config['long_EMA']
        self.delta = config['delta']
        self.fees = config['fees']
        self.print_advice = config['print_advice']

        self.usdAccount = self.starting_USD = config['starting_USD']
        self.btcAccount = 0

        self.indicators = []
        for candle in history:
            self.add_candle(candle)
