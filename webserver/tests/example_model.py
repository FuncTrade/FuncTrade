from base_function.base import GenericTask

class DataFeed(GenericTask):
    pass

class Actor(GenericTask):
    pass

d1 = DataFeed()
a1 = Actor()

d1 >> a1