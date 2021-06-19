import utime
from task import Task
from color_text import ColorText as ct
from machine import I2C, Pin 
#import drivers.bmp180 as bmp180
#import drivers.bmp085 as bmp085
#import drivers.bme280_int as bme280
import drivers.bme680 as bme680


class BME680(Task):
    """
    BME680 breakout board with bmp680 sensor
    
    Pinout:
    BME-680 | ESP32
    VCC | 5V
    GND	| GND
    SCL	| SCL GPIO22
    SDA	| SDA GPIO21

    Usage:
    from BME680 import BME680
    bme680 = BME680(board.display)
    """

    #TODO:

    def __init__(self, display):
        super().__init__(interval = 3000)
        if display:
            self.display = display
        
        print("bmx Sensor init ...")

        scl_pin = const(22)
        sda_pin = const(21)
        print("scl_pin ", scl_pin)
        print("sda_pin ", sda_pin)

        bmx_i2c = I2C(-1, scl=Pin(scl_pin), sda=Pin(sda_pin))
        # bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)

        BMX_VALUES = ["temp", "hum",  "dew"]
        # self.bmx_sensor = bmp180.BMP180(bmx_i2c)
        # self.bmx_sensor = bmp085.BMP085(bmx_i2c)
        self.bmx_sensor = bme680.BME680_I2C(bmx_i2c)

        # self.bmx_sensor.oversample_sett = 2
        # self.bmx_sensor.baseline = 101325

        self.val_history = dict()
        for val in BMX_VALUES:
            self.val_history[val] = list()

    def update(self, scheduler):
        

        temp = self.bmx_sensor.temperature
        hum = self.bmx_sensor.humidity
        gas = self.bmx_sensor.gas
        # FIXME: Luftgüte Index Berechnung fehlt.
        dew = self.dew_point(t = temp, h = hum)
        self.display.text('Taupunkt {dew:4.1f}C'.format(
            dew=dew), 0)
        #print(temp, hum, dew)
        line_out = '{temp:6.1f}C {hum:4.1f}%'.format(
            temp=temp, hum=hum)
        self.display.text(line_out, 1)

        if temp:
            self.insert_history("temp", temp)
        if hum:
            self.insert_history("hum", hum)
        if dew:
            self.insert_history("dew", dew)
        
        for index in range(len(self.val_history["temp"])):
            t = self.val_history["temp"][index]
            h = self.val_history["hum"][index]
            line_out = '{temp:6.1f}C {hum:4.1f}%'.format(
            temp=t, hum=h)
            self.display.text(line_out, index+1)
            

        #for i, val in enumerate(self.val_history["temp"]):
        #    self.display.text("    " + str(val) + " °C", i+1)
            

    def insert_history(self, val, value):
        self.val_history[val].insert(0, value)
        self.val_history[val] = self.val_history[val][:5]


    def dew_point(self, t = None, h = None):
        """
        Compute the dew point temperature for the current Temperature
        and Humidity measured pair
        """
        from math import log
        if t == None:
            t = self.bmx_sensor.temperature
        if h == None:
            h = self.bmx_sensor.humidity
        h = (log(h, 10) - 2) / 0.4343 + (17.62 * t) / (243.12 + t)
        return 243.12 * h / (17.62 - h)