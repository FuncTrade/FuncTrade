from abc import abstractmethod
from typing import Tuple, TypeVar, Generic, List, Union, Dict
from base_function.data import NoData, GenericData
from collections import deque, defaultdict
import logging


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

class GenericTask(Generic[InputT, OutputT]):
    accepted_types: tuple[type, ...] = (object,)
    pipeline: "Pipeline"
    
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline
    
    def __rshift__(self, other: 'GenericTask') -> None:
        return self.pipeline.add_edge(self, other)

    def __lshift__(self, other: 'GenericTask') -> None:
        return self.pipeline.add_edge(other, self)

    @abstractmethod
    def process(self, input: InputT) -> OutputT:
        raise NotImplementedError

class GenericSourceTask(GenericTask[NoData, OutputT]):
    accepted_types = (NoData, )

class GenericActor(GenericTask[InputT, OutputT], Generic[InputT, OutputT]):
    pass

class GenericCalculator(GenericTask[InputT, OutputT], Generic[InputT, OutputT]):
    pass

class Pipeline:
    def __init__(self):
        self.graph = defaultdict(list)   # task -> downstreams(list)
        self.sources = []                # all task instances

    def add_edge(self, src: GenericTask, dst: GenericTask):
        self.graph[src].append(dst)
        self.last_task = dst
        if src not in self.sources and all(src not in v for v in self.graph.values()):
            self.sources.append(src)
    
    def execute(self):
        visited = set()

        def dfs(task: GenericTask, data: GenericData):
            logging.debug("Task {} processing..., input data is {}".format(task.__class__, data.__class__))
            
            if not isinstance(data, task.accepted_types):
                return  # if data type is not accepted, skip
            
            output = task.process(data)

            if isinstance(task, GenericSourceTask):
                while not isinstance(output, NoData):
                    for nxt in self.graph.get(task, []):
                        dfs(nxt, output)
                    output = task.process(NoData())
            else:
                for nxt in self.graph.get(task, []):
                    dfs(nxt, output)

        for src in self.sources:
            if src not in visited:
                dfs(src, NoData())   # Start from NoData

    # def __rshift__(self, other: Union['Pipeline', GenericTask]) -> 'Pipeline':
    #     # 支持 task >> task
    #     if isinstance(other, Pipeline):
    #         raise NotImplementedError("暂不支持 pipeline 嵌套合并")
    #     elif isinstance(other, GenericTask):
    #         self.add_edge(self.last_task, other)
    #         self.last_task = other
    #     return self

    # def __lshift__(self, other: GenericTask) -> 'Pipeline':
    #     self.add_edge(other, self.last_task)
    #     return self

    # @classmethod
    # def from_task(cls, task: GenericTask) -> 'Pipeline':
    #     pipe = cls()
    #     pipe.last_task = task
    #     if task not in pipe.sources:
    #         pipe.sources.append(task)
    #     return pipe

    
