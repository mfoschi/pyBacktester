from datetime import datetime
from average import ExponentialAverage

__author__ = 'Marcello Foschi'

MAX_EMA_SIZE = 30


class PriceCandle():
    def get_previous_values(self, number):
        values = []
        current = self
        for i in range(0, number):
            values.append(current.closing_value)
            if current.previous is not None:
                current = current.previous
        return values

    def __init__(self, date, price, previous):
        self.date = date
        self.closing_value = price
        self.previous = previous
        self.EMAs = {}
        for size in range(1, MAX_EMA_SIZE):
            previous_EMA = None
            if previous is not None:
                previous_EMA = self.previous.EMAs[size]
            self.EMAs[size] = ExponentialAverage(self, size, previous_EMA).value


class Indicator():
    previous = None
    candle = None
    trend = None
    advice = None

    def recalculate_trend(self, tester):
        shortAverage = self.candle.EMAs[tester.short_EMA]
        longAverage = self.candle.EMAs[tester.long_EMA]
        avg = (shortAverage + longAverage) / 2
        diff = 100*(shortAverage - longAverage) / avg
        if diff > tester.delta:
            self.trend = "BULL"
            if tester.current_trend != "BULL":
                self.advice = "BUY"
                tester.current_trend = "BULL"
        else:
            if diff < -tester.delta:
                self.trend = "BEAR"
                if tester.current_trend != "BEAR":
                    self.advice = "SELL"
                    tester.current_trend = "BEAR"
            else:
                self.trend = "HOLD"
                if tester.current_trend is None:
                    # start bullish if no trend yet
                    self.advice = "BUY"
                    tester.current_trend = "BULL"

        if tester.print_advice:
            if self.advice is not None:
                value = self.candle.closing_value
                date = datetime.fromtimestamp(self.candle.date)
                print "advice [%s]: %s at value %s" % (date, self.advice, value)

    def __init__(self, tester, new_candle):
        self.candle = new_candle
        self.recalculate_trend(tester)
