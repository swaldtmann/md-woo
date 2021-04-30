from micropython import const
from machine import Pin
from button import Button


class Beeper():
    """
    Simple pin high for a beeper (EKULIT: AL-60SP05HT)

    Pinout:
    + PIN to GPIO17
    GND PIN GND

    Usage:
    from beeper import Beeper

    beeper = Beeper()
    """

    def __init__(self, io_pin = const(17)):
        print("Beeper init ...")
        self.beeper = Pin(io_pin, Pin.OUT)
        self.beeper_on = False

    def activate_beeper(self):
        print("Activate Beeper with: ", Button.button_a_pressed)
        if Button.button_a_pressed:
            self.beeper_on = True
            self.beeper.on()
        else:
            self.beeper_on = False
            self.beeper.off()

    def deactivate_beeper(self):
        print("Deactivate Beeper")
        self.beeper_on = False
        self.beeper.off()
