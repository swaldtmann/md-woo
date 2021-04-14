from board.metald import Board
from config import Config
from display import Display
from heartbeat import Heartbeat
from task import Scheduler

board = Board()
board.init()

heartbeat = Heartbeat(board.display)

scheduler = Scheduler()

config = Config(board, scheduler)

scheduler.register(board.display)
scheduler.register(heartbeat)

print("Starting scheduler of version {0}".format(config.version))

scheduler.start(100)
