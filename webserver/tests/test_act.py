from unittest import TestCase
from function.act import SingleTickerDailyCloseDataGenerator, DataListCache
from base_function.data import NoData, Data, DataList
import datetime


class TestSingleTickerDailyCloseDataGenerator(TestCase):
    def test_aapl_hist(self):
        generator = SingleTickerDailyCloseDataGenerator(start_at='20100101', end_at='20250801', ticker='AAPL')
        first_result = generator.process(NoData())
        self.assertEqual(first_result, Data(timestamp=datetime.datetime(2010,1,4,0,0), ticker='AAPL', label='Close', value=-1.599))

class TestDataCache(TestCase):
    def test_cache_data(self):
        data_cache = DataListCache(10)

        for i in range(9):
            mock_data = Data(datetime.datetime.now(), 'Mock', 'Mock Label', i)
            out = data_cache.process(mock_data)
            self.assertTrue(isinstance(out, NoData))
        
        final_out = data_cache.process(Data(datetime.datetime.now(), 'Mock', 'Mock Label', -1))

        self.assertTrue(isinstance(final_out, DataList))
        
        if isinstance(final_out, DataList):
            self.assertEqual(final_out.data_list[-1].value, -1)
        
        final_p1_out = data_cache.process(Data(datetime.datetime.now(), 'Mock', 'Mock Label', -2))
        if isinstance(final_p1_out, DataList):
            self.assertEqual(len(final_p1_out.data_list), 10)
            self.assertEqual(final_p1_out.data_list[-2].value, -1)
        else:
            raise