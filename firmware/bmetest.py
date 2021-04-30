#
# Example. Using I2C at P9, P10
#
from machine import I2C, Pin 
from drivers.bme280_int import *
from utime import sleep

scl_pin = const(22)
sda_pin = const(21)

bmp_i2c = I2C(-1, scl=Pin(scl_pin), sda=Pin(sda_pin))
bme280 = BME280(i2c=bmp_i2c)

while True:
    print(bme280.values)
    sleep(1)

