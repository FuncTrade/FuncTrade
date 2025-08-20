import datetime
from dataclasses import dataclass
from typing import List
from function.base import GenericData


@dataclass
class Data(GenericData):
    timestamp: datetime.datetime
    ticker: str
    label: str
    value: float


@dataclass
class Signal(GenericData):
    action: str # buy/sell
    timestamp: datetime.datetime


@dataclass
class DataList(GenericData):
    data_list: List[Data]

class NoData(GenericData):
    pass