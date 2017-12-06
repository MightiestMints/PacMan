
class Dot(object):

    # Constructor assigns location to dot, and boolean for if it is a Big Dot
    def __init__(self, x, y, powerDot):
        self.powerDot = powerDot
        self.location = x, y

    def location(self):
        return self.location

    def powerDot(self):
        return self.powerDot

    def __repr__(self):
        return str("Dot location: " , self.location)