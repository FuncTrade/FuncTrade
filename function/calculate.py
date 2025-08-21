from function.base import GenericCalculator
from function.data import DataList, Data


class MACalculator(GenericCalculator[DataList, Data]):
    def process(self, input: DataList) -> Data:
        total = 0
        for d in input.data_list:
            total += d.value
        
        avg = total / len(input.data_list)
        timestamp = input.data_list[-1].timestamp
        ticker = input.data_list[-1].ticker

        return Data(timestamp=timestamp, ticker=ticker, label='Average', value=avg)
