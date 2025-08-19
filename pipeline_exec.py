from lib.data import DataFeed
from lib.actor import Actor

datafeed = DataFeed(path='data.csv')
actor = Actor(name='main')

datafeed >> actor