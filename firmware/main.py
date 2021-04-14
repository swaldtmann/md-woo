import machine

pin2 = machine.Pin(2, machine.Pin.OUT)

pin2.value(1)




# from board.bohei import Board
# from display import Display
# from name import Name

# network = Network()
# MQTT.init(network)

# board = Board(network)
# board.init()


# heartbeat = Heartbeat(board.display)


# scheduler = Scheduler()

# config = Config(board, network, scheduler)

# name = Name(config, board.display) 
# scheduler.register(board.display)
# scheduler.register(heartbeat)
# scheduler.register(network)
# scheduler.register(MQTT.task)

# print("Starting scheduler of version {0}".format(config.version))

# scheduler.start(100)

