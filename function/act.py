from function.data import Data, DataList, Signal, NoData
from abc import abstractmethod
from typing import Any, List, Union
from .base import GenericActor, GenericData
import datetime
import akshare as ak


class SingleTickerDailyCloseDataGenerator(GenericActor[NoData, Union[NoData, Data]]):
    _records: List[Data]

    def __init__(self, start_at: str, end_at: str, ticker: str) -> None:
        """
        start_at, end_at: %Y%m%d
        """

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


class TradeLogger(GenericActor):
    data: List[Data]
    signal: List[Signal]

    def __init__(self) -> None:
        self.data = []
        self.signal = []

    def log_info(self, info: Union[Data, DataList, Signal, None]) -> None:
        if isinstance(info, Data):
            self.data.append(info)
        elif isinstance(info, DataList):
            self.data.extend(info.data_list)
        elif isinstance(info, Signal):
            self.signal.append(info)
        elif info is None:
            return
        else:
            raise Exception("Unsupport data type: {}".format(type(info)))

    @abstractmethod
    def export(self) -> Any:
        pass


class DataGenerator(GenericActor):
    start_at: datetime.datetime
    end_at: datetime.datetime

    def __init__(self, start_at: datetime.datetime, end_at: datetime.datetime) -> None:
        self.start_at = start_at
        self.end_at = end_at

    @abstractmethod
    def __next__(self) -> Union[Data, DataList, None]:
        pass


