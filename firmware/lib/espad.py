
from utilities import register
from utilities.adapters import peripherals
from utilities.shift_register import ShiftRegister
from signal_generators.ad98xx.ad9850 import *

cls = AD9850

cls.DEBUG_MODE_SHOW_BUS_DATA = False      # whether to show bus data. 
cls.DEBUG_MODE_PRINT_REGISTER = False        # whether to print registers. 

import machine
import gc

gc.collect()

with_hardware_device = True

if with_hardware_device:
    _clk = peripherals.Pin.get_uPy_pin(pin_id = 14, output = True)
    _data = peripherals.Pin.get_uPy_pin(pin_id = 13, output = True)
    _ss = peripherals.Pin.get_uPy_pin(pin_id = 15, output = True)
else:
    _spi = _ss = None  # using None for testing without actual hardware device.

_reset = peripherals.Pin.get_uPy_pin(pin_id = 21, output = True)

lsbfirst = True

_spi = ShiftRegister(stb_pin = _ss, clk_pin = _clk, data_pin = _data, lsbfirst = lsbfirst, polarity = 1)

bus = peripherals.SPI(_spi, _ss, )

ad = AD9850(bus = bus, pin_reset = _reset)

ad.init()

for f in dir(cls):
    if not f.startswith('_'):
        print('ad.{}()'.format(f))

ad.reset()

ad.set_frequency(1.04e7)

ad.enable_output(False)

ad.enable_output(True)

ad.reset()

ad.control_register.print()

ad.print()

cr = ad.control_register
cr_ds = cr.dumps()
cr1 = register.Register('test')
cr1.loads(cr_ds)
cr1.print()

ad.apply_signal()

ad.set_frequency(440)
ad.print()
ad.apply_signal()
ad.enable_output(True)
