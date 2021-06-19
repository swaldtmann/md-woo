from board.metald import Board
from config import Config
from display import Display
from heartbeat import Heartbeat
from task import Scheduler
from CO2 import CO2Sensor
from machine import Pin
from button import Button
from beeper import Beeper
from KY040 import KY040
from BME680 import BME680

HAS_CO2SENSOR = False
HAS_BMXSENSOR = True
HAS_ROTARY = False

board = Board()
board.init()

Button.init(pin=Pin(0, mode=Pin.IN, pull=Pin.PULL_UP))

heartbeat = Heartbeat(board.display)
if HAS_CO2SENSOR:
    beeper = Beeper()
    co2sensor = CO2Sensor(board.display, beeper)
if HAS_BMXSENSOR:
    bmx = BME680(board.display)
if HAS_ROTARY:
    ky040 = KY040(board.display)

scheduler = Scheduler()

config = Config(board, scheduler)

scheduler.register(board.display)

if HAS_CO2SENSOR:
    scheduler.register(co2sensor)
if HAS_BMXSENSOR:
    scheduler.register(bmx)
if HAS_ROTARY:
    scheduler.register(ky040)

scheduler.register(heartbeat)

print("Starting scheduler of version {0}".format(config.version))

scheduler.start(100)
