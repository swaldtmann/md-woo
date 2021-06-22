from board.metald import Board
from config import Config
from heartbeat import Heartbeat
from task import Scheduler
from DHT22 import DHT22

board = Board()
board.init()


heartbeat = Heartbeat(board.display)
dht1 = DHT22(board.display, name='dht_1', pin=13)
dht2 = DHT22(board.display, name='dht_2', pin=17)

scheduler = Scheduler()

config = Config(board, scheduler)

scheduler.register(board.display)

scheduler.register(dht1)
scheduler.register(dht2)

scheduler.register(heartbeat)

print("Starting scheduler of version {0}".format(config.version))

scheduler.start(100)
