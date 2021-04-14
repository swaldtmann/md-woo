from task import Task

class Display(Task):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.lines = [""] * 6
        self.blip = True
        self.interval = 400
        self.clear()

    def text(self, text, line):
        if line > 5:
            raise RuntimeError("You may only access lines 0 to 5.")
        self.lines[line] = text
        self.redraw()

    def show_heartbeat(self, show):
        self.blip = bool(show)
        self.redraw()

    def redraw(self):
        
        if self.driver is None:
            return 

        # Clear display.
        self.driver.fill(0)

        # User-defined lines.
        for row in range(6):
            if self.lines[row] != "":
                self.driver.text(self.lines[row], 0, 8 * row)

        # Status bar.
        self.driver.text("WL " + " ", 16, 57)
        self.driver.text("<3", 113, 57, int(self.blip))

        # Show result and update things.
        self.driver.show()


    def update(self, scheduler):
        mqtt_status = "M"  # FIXME
        wlan_status = "WL"  # FIXME
        self.redraw()

    def clear(self):
        if self.driver is None:
            return 

        self.driver.fill(0)
        self.driver.show()
