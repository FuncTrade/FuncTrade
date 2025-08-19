from abc import abstractmethod
from dataclasses import dataclass
import datetime

from typing import Any, List, Union


@dataclass
class Signal:
    action: str # buy/sell
    timestamp: datetime.datetime


@dataclass
class Data:
    timestamp: datetime.datetime
    ticker: str
    label: str
    value: float


@dataclass
class DataList:
    data_list: List[Data]


class TradeLogger:
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


class DataGenerator:
    start_at: datetime.datetime
    end_at: datetime.datetime

    def __init__(self, start_at: datetime.datetime, end_at: datetime.datetime) -> None:
        self.start_at = start_at
        self.end_at = end_at

    @abstractmethod
    def __next__(self) -> Union[Data, DataList, None]:
        pass


class Trader:
    @abstractmethod
    def signal_act(self, signal: Signal) -> None:
        pass


class Processor:
    @abstractmethod
    def process(self, data: Union[Data, DataList]) -> Union[DataList, Signal, None]:
        pass


class AbstractTask:
    def __rshift__(self, other):
        print(f"{self} >> {other}")
        return (self, other)   # 记录调用关系

    def __lshift__(self, other):
        print(f"{self} << {other}")
        return (other, self)