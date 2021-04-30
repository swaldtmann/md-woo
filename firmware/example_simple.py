# The MIT License (MIT)
# Copyright (c) 2021 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder

import sys
from drivers.rotary_irq_esp import RotaryIRQ

import time


r = RotaryIRQ(pin_num_clk=13,
              pin_num_dt=12,
              min_val=0,
              max_val=5,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)

val_old = r.value()
while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)

    time.sleep_ms(50)
