class Marker():
    def __init__(self):
        # self.L = None
        # self.R = None
        # self.U = None
        # self.D = None
        self.current = None
        self.L = AdjacentProperties()
        self.R = AdjacentProperties()
        self.U = AdjacentProperties()
        self.D = AdjacentProperties()

class AdjacentProperties():
    def __init__(self):
        self.truth = None
        self.cor = None
