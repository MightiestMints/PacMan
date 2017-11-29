import copy as copy
from random import randint

class Ghost(object):

    # Constructor
    def __init__(self, state, respawn):
        self.location = respawn
        self.respawn = respawn

    # Calculates and returns the 2D indices of the ghost spawn location
    def caclulateLocation(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'G':
                    return i, j
        # If it didn't find the location
        print("Could not find ghost spawn point in calculateLocation")
        return None

    # Returns a tuple of the x and y sizes of the state
    def getStateSize(self, state):
        return len(state), len(state[0])

    # Returns variable actions the Ghost has
    def actions(self, state):
        actions = []
        ghostX = self.location[0]
        ghostY = self.location[1]
        stateX = self.getStateSize(state)[0]
        stateY = self.getStateSize(state)[1]

        # Check up
        if (state[ghostX - 1][ghostY] != '=') & (state[ghostX - 1][ghostY] != '|'):
            actions.append("up")
        # Check down
        if (state[ghostX + 1][ghostY] != '=') & (state[ghostX + 1][ghostY] != '|'):
            actions.append("down")
        # Check left
        if (state[ghostX][ghostY - 1] != '|') & (state[ghostX][ghostY - 1] != '='):
            actions.append("left")
        # Check right
        if (state[ghostX][ghostY + 1] != '|') & (state[ghostX][ghostY + 1] != '='):
            actions.append("right")

        return actions

    # Returns the state if an action is taken
    def takeAction(self, state, action):
        newState = copy.deepcopy(state)
        newLoc = None

        # Get location of new position after action is taken
        if action == 'up':
            # check for teloportation
            if state[self.location[0] - 1][self.location[1]] == 't':
                newLoc = (len(state) - 2, self.location[1])
            else:
                newLoc = (self.location[0] - 1, self.location[1])
        elif action == 'down':
            # check for teleportation
            if state[self.location[0] + 1][self.location[1]] == 't':
                newLoc = (1, self.location[1])
            else:
                newLoc = (self.location[0] + 1, self.location[1])
        elif action == 'left':
            # check for telelporation
            if state[self.location[0]][self.location[1] - 1] == 't':
                newLoc = (self.location[0], len(state[0]) - 2)
            else:
                newLoc = (self.location[0], self.location[1] - 1)
        elif action == 'right':
            # check for teleporation
            if state[self.location[0]][self.location[1] + 1] == 't':
                newLoc = (self.location[0], 1)
            else:
                newLoc = (self.location[0], self.location[1] + 1)

        # Update state and location
        #if newState[newLoc[0]][newLoc[1]] != 'G':
        newState[newLoc[0]][newLoc[1]] = 'g'
        #if newState[self.location[0]][self.location[1]] != 'G':
        newState[self.location[0]][self.location[1]] = ' '
        self.location = newLoc
        return newState

    # Causes the ghost to perform a random move every turn
    def randomMove(self, state):
        move = self.actions(state)[randint(0, len(self.actions(state)) - 1)]
        return self.takeAction(state, move)
