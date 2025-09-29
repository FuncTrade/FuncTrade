from base_function.base import GenericCalculator
from base_function.data import DataList, Data, Signal, NoData, DataDict
from typing import Union


class MACalculator(GenericCalculator[DataList, Data]):
    label: str
    accepted_types = (DataList,)

    def __init__(self, label: str) -> None:
        self.label = label

    def process(self, input: DataList) -> Data:
        total = 0
        for d in input.data_list:
            total += d.value
        
        avg = total / len(input.data_list)
        timestamp = input.data_list[-1].timestamp
        ticker = input.data_list[-1].ticker

        return Data(timestamp=timestamp, ticker=ticker, label=self.label, value=avg)
    

class CrossOverSignal(GenericCalculator[DataDict, Union[NoData, Signal]]):
    accepted_types = (DataDict,)
    def process(self, input: DataDict) -> NoData | Signal:
        """
        Only consider 2 MA value and 2 data points
        ma1: short period, ma2: long period
        """
        assert len(input.data_dict.keys()) == 2
        for k in input.data_dict.keys():
            assert len(input.data_dict[k]) == 2

        ma1_values, ma2_values = input.data_dict.values()

        day0_ma1_large = ma1_values[0].value > ma2_values[0].value
        day1_ma1_large = ma1_values[1].value > ma2_values[1].value

        recent_ts = ma1_values[-1].timestamp

        if day0_ma1_large == day1_ma1_large:
            return NoData()
        else:
            if day0_ma1_large == True and day1_ma1_large == False:
                return Signal('sell', recent_ts)
            elif day0_ma1_large == False and day1_ma1_large == True:
                return Signal('buy', recent_ts)
            else:
                return NoData()

        