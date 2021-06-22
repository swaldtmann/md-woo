from task import Task
from color_text import ColorText as ct
from machine import Pin 
from micropython import const
import dht


class DHT22(Task):
    """
    DHT22
    
    Pinout:
    
    Front left to right
    https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/

    DHT22 | ESP32
    1     | 3.3V
    2	  | Pin(22)
    3	  | don't connect
    4	  | GND

    Usage:
    from DHT22 import DHT22
    dht = DHT22(board.display)
    """
    sensor_id = 0

    def __init__(self, display, name='sensor_1', pin=22):
        super().__init__(interval = 2000)
        if display:
            self.display = display
        
        print("DHT Sensor init ...")

        self.name = name
        self.pin = Pin(const(pin))
        DHT22.sensor_id += 1
        self.id = DHT22.sensor_id
        print("Name ", self.name)
        print("Pin ", self.pin)
        print("ID ", DHT22.sensor_id)


        BMP_VALUES = ["temp", "hum"]
        self.dht_sensor = dht.DHT22(self.pin)

        self.val_history = dict()
        for val in BMP_VALUES:
            self.val_history[val] = list()

    def update(self, scheduler):
        self.display.text('DHT Sensor'.format(
            name=self.name
        ), 0)

        self.dht_sensor.measure()
        temp = self.dht_sensor.temperature()
        hum = self.dht_sensor.humidity()
        print('{id:1d}:'.format(
            id=self.id
        ))
        print('{name} Temperature: {temp:4.1f}C'.format(
            name=self.name, temp=temp
        ))
        print('{name} Humidity: {hum:4.1f}C'.format(
            name=self.name, hum=hum
        ))
        
        line_out = 'ID:{id:1d} {temp:4.1f}C {hum:4.1f}%'.format(
            id=self.id, temp=temp, hum=hum)
        self.display.text(line_out, self.id+1)

        if temp:
            self.insert_history("temp", temp)
        if hum:
            self.insert_history("hum", hum)
        
        for index in range(len(self.val_history["temp"])):
            t = self.val_history["temp"][index]
            h = self.val_history["hum"][index]
            line_out = '{temp:6.1f}C {hum:4.1f}%'.format(
            temp=t, hum=h)
            # no history!
            # self.display.text(line_out, index+1)

    def insert_history(self, val, value):
        self.val_history[val].insert(0, value)
        self.val_history[val] = self.val_history[val][:5]
