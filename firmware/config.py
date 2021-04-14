
class Config:
    def __init__(self, board, scheduler):
        self.board = board
        self.scheduler = scheduler
        self.parts_initialized = False
        self.data = {}
        self.mine = None
        self.version = "0.1.0"
