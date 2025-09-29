from unittest import TestCase
from function.calculate import MACalculator
from base_function.data import Data, DataList
from base_function.base import Pipeline
import datetime


class TestMACaculator(TestCase):
    def test_ma_calculator(self):
        pipe = Pipeline()
        d_list = []
        for i in range(5):
            d_list.append(Data(timestamp=datetime.datetime.now(), ticker='Mock', label='Mock Label', value=i))
        
        c_d_list = DataList(d_list)

        ma_cal = MACalculator('MA', pipeline=pipe)

        result = ma_cal.process(c_d_list)

        self.assertEqual(
            result,
            Data(d_list[-1].timestamp, 'Mock', 'MA', 2.0)
        )