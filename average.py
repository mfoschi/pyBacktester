__author__ = 'Marcello Foschi'


class Average(object):
    value = 0


class LinearAverage(Average):
    def __init__(self, candle, size):
        values = candle.get_previous_values(size)
        total = 0
        for value in values:
            total += value

        self.value = total / size


class ExponentialAverage(Average):
    def __init__(self, candle, size, previous_value=None):
        if previous_value is None:
            previous_candle = candle.previous
            if previous_candle is None:
                previous_value = LinearAverage(candle, size).value
            else:
                previous_value = ExponentialAverage(previous_candle, size).value

        multiplier = 2 / float(size + 1)
        current_value = candle.closing_value

        self.value = multiplier * (current_value - previous_value) + previous_value
