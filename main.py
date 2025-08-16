from typing import List, Union, Optional, Any
import datetime
from dataclasses import dataclass
from abc import abstractmethod
import matplotlib.pyplot as plt


@dataclass
class Data:
    timestamp: datetime.datetime
    ticker: str
    label: str
    value: float

@dataclass
class DataList:
    data_list: List[Data]

@dataclass
class Signal:
    action: str # buy/sell
    timestamp: datetime.datetime


class Processor:
    @abstractmethod
    def process(self, data: Union[Data, DataList]) -> Union[DataList, Signal, None]:
        pass

class Trader:
    @abstractmethod
    def signal_act(self, signal: Signal) -> None:
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

class SimplePyplotLogger(TradeLogger):
    def export(self) -> Any:
        fig, ax = plt.subplots()

        values = [dt.value for dt in self.data]
        dts = [dt.timestamp for dt in self.data]

        dots = dict(zip(dts, values))

        ax.plot(dts, values, 'bo')

        for sig in self.signal:
            color = 'g' if sig.action == 'buy' else 'r'
            ax.plot(sig.timestamp, dots[sig.timestamp], color=color)
            ax.annotate(sig.action, (sig.timestamp, dots[sig.timestamp]))
        
        plt.show()
        
# pipeline = DataFeed >> signal_generate >> Actor
