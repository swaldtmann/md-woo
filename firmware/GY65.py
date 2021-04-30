import utime
from task import Task
from color_text import ColorText as ct
from machine import I2C, Pin 
import drivers.bmp180 as bmp180
import drivers.bmp085 as bmp085
import drivers.bme280_int as bme280


class GY65(Task):
    """
    GY-65 breakout board for bmp180 sensor
    
    Pinout:
    GY-65 | ESP32
    VCC | 5V
    GND	| GND
    SCL	| SCL GPIO22
    SDA	| SDA GPIO21

    Usage:
    from GY65 import GY65
    gy65 = GY65(board.display)
    """

    def __init__(self, display):
        super().__init__(interval = 1000)
        if display:
            self.display = display
        
        print("bmp Sensor init ...")

        scl_pin = const(22)
        sda_pin = const(21)
        print("scl_pin ", scl_pin)
        print("sda_pin ", sda_pin)

        bmp_i2c = I2C(-1, scl=Pin(scl_pin), sda=Pin(sda_pin))
        # bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)

        BMP_VALUES = ["temp", "p", "altitude"]
        # self.bmp_sensor = bmp180.BMP180(bmp_i2c)
        self.bmp_sensor = bmp085.BMP085(bmp_i2c)
        self.bmp_sensor.oversample_sett = 2
        self.bmp_sensor.baseline = 101325

        self.ppm_history = dict()
        for val in BMP_VALUES:
            self.ppm_history[val] = list()

    def update(self, scheduler):
        self.display.text("CO2 Sensor ", 0)

        temp = self.bmp_sensor.temperature
        p = self.bmp_sensor.pressure
        altitude = self.bmp_sensor.altitude
        print(temp, p, altitude)

        if temp:
            self.insert_history("temp", temp)
            for i, val in enumerate(self.ppm_history["temp"]):
                self.display.text("    " + str(val) + " °C", i+1)
            

    def insert_history(self, val, value):
        self.ppm_history[val].insert(0, value)
        self.ppm_history[val] = self.ppm_history[val][:5]
