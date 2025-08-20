import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Data:
    timestamp: datetime.datetime
    ticker: str
    label: str
    value: float


@dataclass
class Signal:
    action: str # buy/sell
    timestamp: datetime.datetime


@dataclass
class DataList:
    data_list: List[Data]