from abc import abstractmethod
from dataclasses import dataclass
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd


from typing import Any, List, Union, Optional


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


class SimplePyplotLogger(TradeLogger):
    def export(self) -> Any:
        fig, ax = plt.subplots()

        values = [dt.value for dt in self.data]
        dts = [dt.timestamp for dt in self.data]
        dts = np.array(dts, dtype='datetime64[ns]')

        dots = dict(zip(dts, values))

        ax.plot(dts, values, 'bo')

        sig_dts = [sig.timestamp for sig in self.signal]
        sig_values = [dots[dt] for dt in sig_dts]
        sig_dts = np.array(sig_dts, dtype='datetime64[ns]')

        for i in range(len(sig_dts)):
            action = self.signal[i].action
            x = sig_dts[i]
            y = sig_values[i]
            color = 'g' if action == 'buy' else 'r'
            ax.plot(x, y, color=color)
            ax.annotate(action, (x, y))

        plt.show()


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