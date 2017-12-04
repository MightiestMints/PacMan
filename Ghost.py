import copy as copy
from random import randint

class Ghost(object):

    # Constructor
    def __init__(self, respawn):
        self.onDot = False
        self.location = respawn
        self.respawn = respawn

    # Returns variable actions the Ghost has
    def actions(self, board):
        actions = []
        ghostX = self.location[0]
        ghostY = self.location[1]

        # Check up
        if (board[(ghostX - 1 , ghostY)] != '=') & (board[(ghostX - 1 , ghostY)] != '|'):
            actions.append("up")
        # Check down
        if (board[(ghostX + 1 , ghostY)] != '=') & (board[(ghostX + 1 , ghostY)] != '|'):
            actions.append("down")
        # Check left
        if (board[(ghostX , ghostY - 1)] != '|') & (board[(ghostX , ghostY - 1)] != '='):
            actions.append("left")
        # Check right
        if (board[(ghostX, ghostY + 1)] != '|') & (board[(ghostX , ghostY + 1)] != '='):
            actions.append("right")

        return actions

    # Returns the state if an action is taken
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
                board.move(self.location[0], board.length - 2)
            else:
                board.move(self, self.location[0], self.location[1] - 1)
        elif action == 'right':
            #check for teleportation
            if board[(self.location[0] , self.location[1] + 1)] == 't':
                board.move(self, self.location[0],1)
            else:
                board.move(self, self.location[0], self.location[1] + 1)

    # Causes the ghost to perform a random move every turn
    def randomMove(self, board):
        move = self.actions(board)[randint(0, len(self.actions(board)) - 1)]
        return self.takeAction(board, move)

    # Returns the move that takes Ghost closest to Pacman
    def takeActionShortestDistance(self, board, locOfPacman):

        #Positive means we want to move Right
        xDiff = locOfPacman[1] - self.location[1]
        #Positive means we want to move Down
        yDiff = locOfPacman[0] - self.location[0]

        for action in Ghost.actions(self,board):
            if (action == 'up') & (yDiff < 0):
                return Ghost.takeAction(self, board, action)
            if (action == 'left') & (xDiff < 0):
                return Ghost.takeAction(self, board, action)
            if (action == 'down') & (yDiff > 0):
                return Ghost.takeAction(self, board, action)
            if (action == 'right') & (xDiff > 0):
                return Ghost.takeAction(self, board, action)
        print("Taking random action from takeActionShortestDistance")
        return Ghost.randomMove(self, board)

    # Helps Intelligent Move in finding the best direction to take to get to Pacman
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
            resultBoard = copy.deepcopy(copyBoard)
            result = Ghost.depthLimitedSearch(copySelf, copyBoard, locOfPacman, actions, takeAction, depthLimit-1)
            if result is "cutoff":
                cutOffOccurred = True
            elif result is not "failure":
                result.insert(0, resultBoard)
                return result
        if cutOffOccurred:
            return "cutoff"
        else:
            return "failure"

    # Causes the ghost to scan through the board, making the most intelligent shortest path decision
    def intelligentMove(self, board, locOfPacman, maxDepth=4):
        if self.location == locOfPacman:
            return
        for depth in range(maxDepth):
            result = Ghost.depthLimitedSearch(self, board, locOfPacman, Ghost.actions, Ghost.takeAction, depth)
            if result != "cutoff" and result != "failure":
                print("Ghost found intelligent move. Returning intelligentMove")
                print("My new location: ", self.location)
                return result
        # If we get here, this means we were cutoff. Essentially, we couldn't find Pacman within maxDepth moves
        # At this point, we just want to make a move in the direction that Pacman is in
        return Ghost.takeActionShortestDistance(self, board, locOfPacman)