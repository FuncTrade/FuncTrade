from base_function.base import GenericTask, Pipeline

# pyright: reportUnusedExpression=false

class DataFeed(GenericTask):
    pass

class Actor(GenericTask):
    pass

pipe = Pipeline()

d1 = DataFeed(pipe)
a1 = Actor(pipe)

d1 >> a1