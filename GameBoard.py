
class Dot(object):

    # Constructor assigns location to dot, and boolean for if it is a Big Dot
    def __init__(self, x, y, powerDot):
        self.powerDot = powerDot
        self.location = x, y

    def location(self):
        return self.location

    def powerDot(self):
        return self.powerDot


class GameBoard(object):


    #Constructor (Work in progress)
    def __init__(self, startState):
        self.board = startState

        return

    def __getitem__(self, item):
        x = item[0]
        y = item[1]
        return self.board[x][y]


    def getDots(self, state):
        dots = []
        for x, i in enumerate(state):
            for y, j in enumerate(state[x]):
                if j is '.':
                    dots.append(Dot(x, y, False))
                if j is 'o':
                    dots.append(Dot(x, y, True))
        return dots