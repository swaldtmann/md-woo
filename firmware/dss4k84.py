
from utilities import register
from utilities.adapters import peripherals
from utilities.shift_register import ShiftRegister
from signal_generators.ad98xx.ad9850 import *

import machine
import gc

gc.collect()

_clk = peripherals.Pin.get_uPy_pin(pin_id = 14, output = True)
_data = peripherals.Pin.get_uPy_pin(pin_id = 13, output = True)
_ss = peripherals.Pin.get_uPy_pin(pin_id = 15, output = True)
_spi = ShiftRegister(stb_pin = _ss, clk_pin = _clk, data_pin = _data, lsbfirst = True, polarity = 1)
bus = peripherals.SPI(_spi, _ss, )

_reset = peripherals.Pin.get_uPy_pin(pin_id = 21, output = True)
ad = AD9850(bus = bus, pin_reset = _reset)
ad.reset()

ad.set_frequency(4.84e3)
