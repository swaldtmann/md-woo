import time

from micropython import const
from machine import Pin, Timer


BUTTON_A_PIN = const(0)
# BUTTON_B_PIN = const(35)  # Reset button!


class Button():
    """
    Debounced pin handler for toggle state

    Usage:
    from machine import Pin
    from button import Button
    
    Button.init(pin=Pin(0, mode=Pin.IN, pull=Pin.PULL_UP))
    """

    @classmethod
    def init(cls, pin, trigger=Pin.IRQ_FALLING, min_ago=300):
        cls.button_a_pressed = False

        cls.callback = cls.button_a_callback
        cls.min_ago = min_ago

        cls._blocked = False
        cls._next_call = time.ticks_ms() + cls.min_ago

        pin.irq(trigger=trigger, handler=cls.debounce_handler)


    @classmethod
    def call_callback(cls, pin):
        cls.callback(pin)

    @classmethod
    def button_a_callback(cls, pin):
        """Toggle cls.button_a_pressed state"""
        if cls.button_a_pressed == True:
            cls.button_a_pressed = False
        else:
            cls.button_a_pressed = True
        print("Button A (%s) changed to: %r" % (pin, cls.button_a_pressed))

    @classmethod
    def debounce_handler(cls, pin):
        if time.ticks_ms() > cls._next_call:
            cls._next_call = time.ticks_ms() + cls.min_ago
            cls.call_callback(pin)
        else:
            print("debounce: %s" % (cls._next_call - time.ticks_ms()))
        