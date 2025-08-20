from abc import abstractmethod
from typing import Union, Tuple, TypeVar, Generic


class GenericData:
    pass

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

class GenericTask(Generic[InputT, OutputT]):
    def __rshift__(self, other) -> Tuple['GenericTask', 'GenericTask']:
        print(f"{self} >> {other}")
        return (self, other)   # 记录调用关系

    def __lshift__(self, other) -> Tuple['GenericTask', 'GenericTask']:
        print(f"{self} << {other}")
        return (other, self)
    
    @abstractmethod
    def process(self, input: InputT) -> OutputT:
        pass

class GenericActor(GenericTask[InputT, OutputT], Generic[InputT, OutputT]):
    pass

class GenericCalculator(GenericTask[InputT, OutputT], Generic[InputT, OutputT]):
    pass