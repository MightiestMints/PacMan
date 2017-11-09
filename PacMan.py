
# Implements the learning algorithms that pac-man will use to manuever through the game board, and avoid ghost/eat dots
# 3 class variables: lives (remaining lives), dotsLeft (dots remaining on the board), & location (2D list index of PacMan)
class PacMan(object):

    # Constructor
    def __init__(self, state):
        self.lives = 3
        self.dotsLeft = self.calculateDotsLeft(state)
        self.location = self.calculateLocation(state)

    # Returns all possible actions (up, down, left, right)
    def actions(self, state):
        actions = []
        pacX = self.location[0]
        pacY = self.location[1]
        stateX = self.getStateSize(state)[0]
        stateY = self.getStateSize(state)[1]
        # Check up
        if (pacX - 1 != 0) & (state[pacX - 1][0][pacY] != '='):
            actions.append("up")
        # Check down
        if (pacX + 1 != stateX - 1) & (state[pacX + 1][0][pacY] != '='):
            actions.append("down")
        # Check left
        if (pacY - 1 != 0) & (state[pacX][0][pacY - 1] != '|'):
            actions.append("left")
        # Check right
        if (pacY + 1 != stateY - 1) & (state[pacX][0][pacY + 1] != '|'):
            actions.append("right")

        return actions

    # Returns a tuple containing (state after an action is taken,
    def takeAction(self, state, action):
        newState = state[:]
        newLoc = None

        # Get location of new position after action is taken
        if action == 'up':
            newLoc = (self.location[0] - 1, self.location[1])
        elif action == 'down':
            newLoc = (self.location[0] + 1, self.location[1])
        elif action == 'left':
            newLoc = (self.location[0], self.location[1] - 1)
        elif action == 'right':
            newLoc = (self.location[0], self.location[1] + 1)

        # Update class variables
        s = newState[newLoc[0]][0][newLoc[1]]
        if s == '.':
            self.dotsLeft -= 1
        if s == 'g':
            self.lives -= 1
            print("You died")                # TODO (Respawn after Pac Man hits a ghost)

        # Update state and location
        if newState[newLoc[0]][0][newLoc[1]] != 'P':
            row1 = newState[newLoc[0]][0][:newLoc[1]]
            row2 = newState[newLoc[0]][0][(newLoc[1] + 1):]
            row = row1 + 'p' + row2
            newState[newLoc[0]][0] = row
        if newState[self.location[0]][0][self.location[1]] != 'P':
            row1 = newState[self.location[0]][0][:self.location[1]]
            row2 = newState[self.location[0]][0][(self.location[1] + 1):]
            row = row1 + ' ' + row2
            newState[self.location[0]][0] = row
        self.location = newLoc
        return newState

    # Returns a tuple of the x and y sizes of the state
    def getStateSize(self, state):
        return (len(state), len(state[0][0]))

    # Calculates and returns the 2D list location of PacMan, or, if he hasn't spawned yet, his spawn point
    # Should only be called by constructor (location updated in takeAction)
    def calculateLocation(self, state):
        spawnLoc = None
        currentLoc = None
        for i in range(len(state)):
            for j in range(len(state[i][0])):
                if state[i][0][j] == 'P':
                    spawnLoc = (i, j)
                elif state[i][0][j] == 'p':
                    currentLoc = (i, j)
        if currentLoc != None:
            return currentLoc
        else: return spawnLoc


    # Calculates and returns the number of dots in a given state.
    # Should only be called by constructor (dotsLeft updated in takeAction)
    def calculateDotsLeft(self, state):
        dots = 0
        for i in range(len(state)):
            for j in range(len(state[i][0])):
                if state[i][0][j]  == '.':
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

    # Returns the amount of lives Pac Man has left
    def getLives(self):
        return self.lives