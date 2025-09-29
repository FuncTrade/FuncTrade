import datetime
from dataclasses import dataclass
from typing import List, Dict

class GenericData:
    pass

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

@dataclass
class NoData(GenericData):
    pass

@dataclass
class DataDict(GenericData):
    data_dict: Dict[str, List[Data]]