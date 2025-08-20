from unittest import TestCase
from function.act import SingleTickerDailyCloseDataGenerator
from function.data import NoData, Data
import datetime


class TestSingleTickerDailyCloseDataGenerator(TestCase):
    def test_aapl_hist(self):
        generator = SingleTickerDailyCloseDataGenerator(start_at='20100101', end_at='20250801', ticker='AAPL')
        first_result = generator.process(NoData())
        self.assertEqual(first_result, Data(timestamp=datetime.datetime(2010,1,4,0,0), ticker='AAPL', label='Close', value=-1.599))