from datetime import datetime, timedelta
import unittest

from average import LinearAverage, ExponentialAverage
from prices import PriceCandle


class AverageTest(unittest.TestCase):
    test_candles = []

    def setUp(self):
        last_date = datetime(2013, 1, 1)
        last_candle = None
        values = [109.59, 109.634, 107.89, 109.47, 108.5, 108.131, 109.3, 109.49, 107.892, 107.5]
        for value in values:
            candle = PriceCandle(last_date, value, last_candle)
            self.test_candles.append(candle)
            last_candle = candle
            last_date += timedelta(hours=1)

    def test_linear_single(self):
        """
        Tests that linear average of a single candle is its closing value.
        """
        sample_candle = self.test_candles[0]
        average = LinearAverage(sample_candle, 1).value
        self.assertEquals(average, sample_candle.closing_value)

    def test_linear_simple(self):
        """
        Tests that linear average of n candles is sum of values / n.
        """
        sample_candle = self.test_candles[9]
        average = LinearAverage(sample_candle, 10).value
        self.assertAlmostEquals(average, 108.74, 2)

    def test_exp_single(self):
        """
        Tests that exponential average of a single candle is its closing value.
        """
        sample_candle = self.test_candles[0]
        average = ExponentialAverage(sample_candle, 1).value
        self.assertEquals(average, sample_candle.closing_value)

    def test_exp_simple(self):
        """
        Tests the exponential average of n candles.
        """
        sample_candle = self.test_candles[9]
        average = ExponentialAverage(sample_candle, 10).value
        self.assertAlmostEqual(average, 108.64, 2)


if __name__ == "__main__":
    unittest.main()
