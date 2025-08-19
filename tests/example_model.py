from func.base import AbstractTask

class DataFeed(AbstractTask):
    pass

class Actor(AbstractTask):
    pass

d1 = DataFeed()
a1 = Actor()

d1 >> a1