
# Implements the learning algorithms that pac-man will use to manuever through the game board, and avoid ghost/eat dots
# 2 class variables: lives (remaining lives), dotsLeft (dots remaining on the board)
class PacMan(object):

    # Constructor
    def __init__(self, state):
        self.lives = 3
        self.dotsLeft = self.calculateDotsLeft(state)

    # Calculates and returns the number of dots in a given state.
    def calculateDotsLeft(self, state):
        dots = 0
        for i in range(len(state)):
            for j in range(len(state[i][0])):
                s = state[i][0][j]
                if s == '.':
                    dots += 1
        return dots

    # Returns the dots left on the board
    def dotsLeft(self):
        return self.dotsLeft

    # Prints the current state to the console. Takes in a 2D list of any size as a parameter
    def printState(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                print(state[i][j], end='')
            print()

    # Returns true if the game is over (pac-man is eaten by a ghost or has eaten all the dots) or false if not over
    def gameOver(self):
        return (self.lives == 0) | (self.dotsLeft == 0)