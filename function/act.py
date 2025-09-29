import matplotlib.pyplot as plt
import numpy as np
from base_function.data import Data, DataList, Signal, NoData, DataDict
from abc import abstractmethod
from typing import Any, List, Union, Dict

from base_function.data import GenericData
from base_function.base import GenericActor, GenericSourceTask, Pipeline
import datetime
import akshare as ak
from collections import deque


class SingleTickerDailyCloseDataGenerator(GenericActor[NoData, Union[NoData, Data]], GenericSourceTask):
    _records: List[Data]

    def __init__(self, start_at: str, end_at: str, ticker: str, pipeline: Pipeline) -> None:
        """
        start_at, end_at: %Y%m%d
        """
        super().__init__(pipeline)

        symbol = '105.' + ticker
        stock_us_hist_df = ak.stock_us_hist(symbol=symbol, period="daily", start_date=start_at, end_date=end_at, adjust="qfq")
        stock_us_hist_df = stock_us_hist_df.sort_index(ascending=False)

        records = stock_us_hist_df.to_dict(orient='records')
        self._records = [
            Data(
                timestamp=datetime.datetime.strptime(d['日期'], "%Y-%m-%d"),
                ticker=ticker,
                label='Close',
                value=d['收盘']
            )
            for d in records
        ]
    
    def process(self, input: NoData) -> Union[NoData, Data]:
        if len(self._records) > 0:
            return self._records.pop()
        else:
            return NoData()

class DataListCache(GenericActor[Data, Union[DataList, NoData]]):
    _deque: deque
    _max_length: int

    def __init__(self, max_length: int, pipeline: Pipeline) -> None:
        super().__init__(pipeline)
        self._deque = deque([], maxlen=max_length)
        self._max_length = max_length
    
    def process(self, input: Data) -> DataList | NoData:
        self._deque.append(input)
        if len(self._deque) == self._max_length:
            return DataList(list(self._deque.copy()))
        else:
            return NoData()

class DataDictCache(GenericActor[Data, Union[DataDict, NoData]]):
    data_dict: Dict[str, deque]
    len_dict: Dict[str, int]

    def __init__(self, len_dict: Dict[str, int], pipeline: Pipeline) -> None:
        super().__init__(pipeline)
        self.len_dict = len_dict.copy()
        self.data_dict = {k: deque(maxlen=len_dict[k]) for k in len_dict.keys()}
    
    def process(self, input: Data) -> DataDict | NoData:
        if input.label in self.data_dict.keys():
            self.data_dict[input.label].append(input)
        
        for k in self.len_dict.keys():
            if len(self.data_dict[k]) < self.len_dict[k]:
                return NoData()
        
        out = {k: list(self.data_dict[k]) for k in self.data_dict.keys()}
        return DataDict(out)       


class TradeLogger(GenericActor):
    data: List[Data]
    signal: List[Signal]
    accepted_types = (Data, DataList, Signal)

    def __init__(self, pipeline: Pipeline) -> None:
        super().__init__(pipeline)
        self.data = []
        self.signal = []

    def process(self, input: Union[Data, DataList, Signal]) -> None:
        if isinstance(input, Data):
            self.data.append(input)
        elif isinstance(input, DataList):
            self.data.extend(input.data_list)
        elif isinstance(input, Signal):
            self.signal.append(input)
        else:
            raise Exception("Unsupport data type: {}".format(type(input)))

    @abstractmethod
    def export(self) -> Any:
        pass


class SimplePyplotLogger(TradeLogger):
    def export(self) -> Any:
        fig, ax = plt.subplots()

        values = [dt.value for dt in self.data]
        dts = [dt.timestamp for dt in self.data]
        dts = np.array(dts)

        dots = dict(zip(dts, values))

        ax.plot(dts, values, 'b-', label="Price")

        sig_dts = [sig.timestamp for sig in self.signal]
        sig_values = [dots[dt] for dt in sig_dts]
        sig_dts = np.array(sig_dts)

        for i in range(len(sig_dts)):
            action = self.signal[i].action
            x = sig_dts[i]
            y = sig_values[i]
            color = 'g' if action == 'buy' else 'r'
            ax.plot(x, y, marker='o', color=color)
            ax.annotate(action, (x, y))

        plt.show()


