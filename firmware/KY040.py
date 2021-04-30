from task import Task
from drivers.rotary_irq_esp import RotaryIRQ



class KY040(Task):
    """
    KY-040 Rotary Encoder
    
    Pinout:
    KY-040 | ESP32
    VCC | 5V
    GND	| GND
    CLK	| GPIO13
    DT	| GPIO12
    SW  | Button GPIO0


    Usage:
    from KY040 import KY040

    rotary = KY040(board.display)
    """

    def __init__(self, display):
        super().__init__(interval = 50)
        if display:
            self.display = display
        
        print("Rotary Knob init ...")
        self.knob = RotaryIRQ(pin_num_clk=13,
              pin_num_dt=12,
              min_val=0,
              max_val=5,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)
        self.val_new = 0
        self.val_old = self.knob.value()


    def update(self, scheduler):
        self.display.text("CO2 Sensor ", 0)

        self.val_new = self.knob.value()

        if self.val_old != self.val_new:
            self.val_old = self.val_new
            print('result =', self.val_new)
            self.display.text("Knob: " + str(self.val_new), 1)

