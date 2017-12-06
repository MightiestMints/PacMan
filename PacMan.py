import copy as copy
import numpy as np

# Implements the learning algorithms that pac-man will use to manuever through the game board, and avoid ghost/eat dots
# 3 class variables: lives (remaining lives), dotsLeft (dots remaining on the board), & location (2D list index of PacMan)
class PacMan(object):

    # Constructor
    def __init__(self, respawn):
        self.lives = 3                                      # Lives left
        self.location = respawn                             # 2D indices of Pac Man's location
        self.respawn = respawn                              # 2D indices of Pac Man's spawn point

    # Return spawn point for PacMan
    def spawnPt(self):
        return self.respawn

    # Returns all possible actions (up, down, left, right)
    def actions(self, board):
        actions = []
        pacX = self.location[0]
        pacY = self.location[1]

        # Check up
        if (board[(pacX - 1 , pacY)] != '=') & (board[(pacX - 1 , pacY)] != '|'):
            actions.append("up")
        # Check down
        if (board[(pacX + 1 , pacY)] != '=') & (board[(pacX + 1 , pacY)] != '|'):
            actions.append("down")
        # Check left
        if (board[(pacX , pacY - 1)] != '|') & (board[(pacX , pacY - 1)] != '='):
            actions.append("left")
        # Check right
        if (board[(pacX , pacY + 1)] != '|') & (board[(pacX , pacY + 1)] != '='):
            actions.append("right")

        return actions

    # Returns a tuple containing (state after an action is taken,
    def takeAction(self, board, action):

        # Get location of new position after action is taken
        if action == 'up':
            #check for teleportation
            if board[(self.location[0] - 1 , self.location[1])] == 't':
                board.move( self , board.height - 2, self.location[1])
            else:
                board.move( self, self.location[0] - 1, self.location[1])
        elif action == 'down':
            #check for teleportation
            if board[(self.location[0] + 1,self.location[1])] == 't':
                board.move(self, 1, self.location[1])
            else:
                board.move(self, self.location[0] + 1, self.location[1])
        elif action == 'left':
            #check for teleportation
            if board[(self.location[0] , self.location[1] - 1)] == 't':
                board.move(self, self.location[0], board.length - 2)
            else:
                board.move(self, self.location[0], self.location[1] - 1)
        elif action == 'right':
            #check for teleportation
            if board[(self.location[0] , self.location[1] + 1)] == 't':
                board.move(self, self.location[0],1)
            else:
                board.move(self, self.location[0], self.location[1] + 1)

    # Returns the move that takes Ghost closest to Pacman
    def calculateDistance(self, dot):
        # Positive means we want to move Right
        xDiff = dot.location[1] - self.location[1]
        # Positive means we want to move Down
        yDiff = dot.location[0] - self.location[0]

        return np.abs(xDiff) + np.abs(yDiff)

    def getClosestDots(self, board):
        dots = board.getDots()
        closestDots = []
        min = self.calculateDistance(dots[0])
        for dot in dots:
            if self.calculateDistance(dot) < min:
                closestDots.append(dot)
                min = self.calculateDistance(dot)
                print(dot)
            if self.calculateDistance(dot) == min:
                closestDots.append(dot)
                print(dot)

    # PacMan "blood hunter" AI. Copied from Ghost.
    # Helps Intelligent Move in finding the best direction to take to get to nearest dot
    def depthLimitedSearch(self, board, locOfPacman, actions, takeAction, depthLimit):
        if self.location == locOfPacman:
            return []

        if depthLimit == 0:
            return "cutoff"

        cutOffOccurred = False
        for action in actions(self, board):
            copyBoard = copy.deepcopy(board)
            copySelf = copy.deepcopy(self)
            takeAction(copySelf, copyBoard, action)
            result = Ghost.depthLimitedSearch(copySelf, copyBoard, locOfPacman, actions, takeAction,
                                              depthLimit - 1)
            if result is "cutoff":
                cutOffOccurred = True
            elif result is not "failure":
                return action
        if cutOffOccurred:
            return "cutoff"
        else:
            return "failure"

    # Causes the ghost to scan through the board, making the most intelligent shortest path decision
    def intelligentMove(self, board, locOfPacman, maxDepth=4):
        if self.location == locOfPacman:
            return
        for depth in range(maxDepth):
            result = Ghost.depthLimitedSearch(self, board, locOfPacman, Ghost.actions, Ghost.takeAction,
                                              depth)
            if result != "cutoff" and result != "failure":
                print("Ghost found intelligent move. Returning intelligentMove")
                return Ghost.takeAction(self, board, result)
        # If we get here, this means we were cutoff. Essentially, we couldn't find Pacman within maxDepth moves
        # At this point, we just want to make a move in the direction that Pacman is in
        print("Ghost didn't find intelligent move. Running takeActionShortestDistance")
        return Ghost.takeActionShortestDistance(self, board, locOfPacman)


    # Returns true if the game is over (pac-man is eaten by a ghost or has eaten all the dots) or false if not over
    def gameOver(self, board):
        return (self.lives == 0) | (board.dotsLeft == 0)

    # Returns the amount of lives Pac Man has left
    def getLives(self):
        return self.lives