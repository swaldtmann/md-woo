import utime
from task import Task
from color_text import ColorText as ct
import drivers.mhz14a as mhz14a


class CO2Sensor(Task):
    """
    CO2 Sensor
    MH-Z14A
    
    Pinout:
    RX PIN on Sensor to GPIO18
    TX PIN on Sensor to GPIO19

    Usage:
    from CO2 import CO2Sensor
    co2sensor = CO2Sensor(board.display)
    """
    def __init__(self, display, beeper):
        super().__init__(interval = 5000)
        if display:
            self.display = display
        
        print("CO2 Sensor init ...")
        self.co2_sensor = mhz14a.MHZ14A(uartNum=1, rxPin=18, txPin=19)
        self.ppm_history = list()
        self.init_utime = utime.time()
        self.warmup_seconds = 180
        self.warmup = True
        self.beeper = beeper
        self.beeper_threshold = 1000  # Beeper on above 1000 ppm
        
    def update(self, scheduler):
        self.display.text("CO2 Sensor ",0)

        if self.warmup:
            wait_time = self.init_utime + self.warmup_seconds - utime.time()
            if wait_time > 0:
                self.display.text("    Warmup!", 2)
                self.display.text("    Waiting", 3)
                self.display.text("    " + str(wait_time) + " seconds", 4)
            else:
                self.warmup = False
                for i in range(1, 5):
                    self.display.text("", i)
            return
        
        ppm = 0
        ppm = self.co2_sensor.readCO2()

        if ppm > 0:
            if ppm > self.beeper_threshold:
                self.beeper.activate_beeper()
            else:
                self.beeper.deactivate_beeper()
            self.insert_history(ppm)
            for i, val in enumerate(self.ppm_history):
                self.display.text(self.get_air_quality(val) + " " + str(val) + " ppm", i+1)
            
    def get_air_quality(self, ppm):
        air_quality = "??? "
        if ppm <= 800:
            air_quality = "Well"
        elif ppm <= 1000:
            air_quality = "Good"
        elif ppm <= 1400:
            air_quality = "Poor"
        else:
            air_quality = "Bad "
        return air_quality

    def insert_history(self, value):
        self.ppm_history.insert(0, value)
        self.ppm_history = self.ppm_history[:5]