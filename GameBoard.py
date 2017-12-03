import PacMan as P
import Ghost as G
import copy

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
        self.board = copy.deepcopy(startState)
        self.dots = self.getDots(startState)
        self.ghostSpawnPt = self.findGhostSpawnPt(startState)
        self.pacManSpawnPt = self.findPacManSpawnPt(startState)
        self.height = len(startState)
        self.length = len(startState[0])
        self.dotsLeft = self.calculateDotsLeft(startState)
        return

    def __getitem__(self, item):
        x = item[0]
        y = item[1]
        return self.board[x][y]

    def findGhostSpawnPt(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'G':
                    return i, j
        # If it didn't find the location
        print("Could not find ghost spawn point in calculateLocation")
        return None

    def findPacManSpawnPt(self, state):
        spawnLoc = None
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'P':
                    spawnLoc = i, j
        return spawnLoc

    def getDots(self, state):
        dots = []
        for x, i in enumerate(state):
            for y, j in enumerate(state[x]):
                if j is '.':
                    dots.append(Dot(x, y, False))
                if j is 'o':
                    dots.append(Dot(x, y, True))
        return dots

    def __str__(self):
        value = ''
        for i in range(len(self.board)):
             for j in range(len(self.board[i])):
                value += self.board[i][j]
             value += '\n'
        return value

    # Calculates and returns the number of dots in a given state.
    # Should only be called by constructor (dotsLeft updated in takeAction)
    def calculateDotsLeft(self, state):
        dots = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j]  == '.':
                    dots += 1
        return dots

    def move(self, target, x, y):
        tarX = target.location[0]
        tarY = target.location[1]
        if isinstance(target, P.PacMan):
            if self.board[x][y] is '.':
             self.dotsLeft = self.dotsLeft - 1
             self.board[x][y] = 'p'
             self.board[tarX][tarY] = ' '
             target.location = x,y
            else:
             self.board[x][y] = 'p'
             self.board[tarX][tarY] = ' '
             target.location = x,y
        else:
            print("should not be in here"
                  "")