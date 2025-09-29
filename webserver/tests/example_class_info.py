from base_function.base import GenericCalculator, Pipeline
from base_function.data import Data, DataList


class MACalculator(GenericCalculator[DataList, Data]):
    label: str
    accepted_types = (DataList,)

    def __init__(self, label: str, pipeline: Pipeline) -> None:
        super().__init__(pipeline)
        self.label = label

    def process(self, input: DataList) -> Data:
        total = 0
        for d in input.data_list:
            total += d.value
        
        avg = total / len(input.data_list)
        timestamp = input.data_list[-1].timestamp
        ticker = input.data_list[-1].ticker

        return Data(timestamp=timestamp, ticker=ticker, label=self.label, value=avg)