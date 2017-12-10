import copy as copy
import random
import numpy as np
import PlayGame as PlayGame

# Implements the learning algorithms that pac-man will use to maneuver through the game board, and avoid ghost/eat dots
# 3 class variables: lives (remaining lives), dotsLeft (dots remaining on the board), & location (2D list index of PacMan)
class PacMan(object):

    # Constructor
    def __init__(self, respawn):
        self.lives = 3                                     # Lives left
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
        if (board.board[pacX - 1][pacY] != '=') & (board.board[pacX - 1][pacY] != '|'):
            actions.append("up")
        # Check down
        if (board.board[pacX + 1][pacY] != '=') & (board.board[pacX + 1][pacY] != '|'):
            actions.append("down")
        # Check left
        if (board.board[pacX][pacY - 1] != '|') & (board.board[pacX][pacY - 1] != '='):
            actions.append("left")
        # Check right
        if (board.board[pacX][pacY + 1] != '|') & (board.board[pacX][pacY + 1] != '='):
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

    # Returns a value representing manhattan distance from pacman.
    def calculateDistance(self, obj):
        # Positive means we want to move Right
        xDiff = obj.location[1] - self.location[1]
        # Positive means we want to move Down
        yDiff = obj.location[0] - self.location[0]

        return np.abs(xDiff) + np.abs(yDiff)

    # Returns a list of closest dots to PacMan
    def getClosestDots(self, board):
        dots = board.getDots()
        closestDots = []
        min = self.calculateDistance(dots[0])
        for dot in dots:
            if self.calculateDistance(dot) < min:
                closestDots.append(dot)
                min = self.calculateDistance(dot)
            if self.calculateDistance(dot) == min:
                closestDots.append(dot)
        return closestDots

    # Returns the directions to avoid if ghost is too close
    def directionToObj(self, obj):
        directions = []
        x = self.location[0] - obj.location[0]
        y = self.location[1] - obj.location[1]

        if x > 0:
            directions.append('up')
        if x < 0:
            directions.append('down')
        if y > 0:
            directions.append('left')
        if y < 0:
            directions.append('right')

        return directions

    # Returns true if ghost is within manhattan distance of 3 from pacman
    def fearFactor(self, ghosts):
        for ghost in ghosts:
            distance = self.calculateDistance(ghost)
            if(distance < 3):
                return True
            else:
                return False


    # PacMan "blood hunter" AI. Copied from Ghost.
    # Helps Intelligent Move in finding the best direction to take to get to nearest dot
    def depthLimitedSearch(self, board, ghosts, closestDots, actions, takeAction, depthLimit):
        if PacMan.fearFactor(self, ghosts):
            return 'run'

        for dot in closestDots:
            if self.location == dot.location:
                return []

        if depthLimit == 0:
            return "cutoff"

        cutOffOccurred = False
        for action in PacMan.actions(self, board):
            copyBoard = copy.deepcopy(board)
            copySelf = copy.deepcopy(self)
            takeAction(copySelf, copyBoard, action)
            result = PacMan.depthLimitedSearch(copySelf, copyBoard, ghosts, closestDots, actions, takeAction,
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
    def intelligentMove(self, board, ghosts, maxDepth=4):
        closestDots = PacMan.getClosestDots(self, board)

        for dot in closestDots:
            if self.location == dot.location:
                return

        for depth in range(maxDepth):
            result = PacMan.depthLimitedSearch(self, board, ghosts, closestDots, PacMan.actions, PacMan.takeAction,
                                              depth)
            if result != "cutoff" and result != "failure" and result != 'run':
                print("PacMan found intelligent move. Returning intelligentMove")
                return PacMan.takeAction(self, board, result)

        if(result == 'run'):
            PacMan.runFromGhost(self, board, ghosts,  PacMan.actions)
        else:
            PacMan.makeRandomMove(self, board)

    def runFromGhost(self, board, ghosts, actions):
        print("running from ghosts")
        listOfActions = PacMan.actions(self, board)
        for ghost in ghosts:
            #Find direction towards ghost, avoid it...
            directions = self.directionToObj(ghost)
            for direction in directions:
                for action in listOfActions:
                    if action == direction:
                        listOfActions.remove(direction)
        if(listOfActions):
            PacMan.takeAction(self, board, np.random.choice(listOfActions))
        else:
            PacMan.makeRandomMove(self, board)

    def makeRandomMove(self, board):
        PacMan.takeAction(self, board, PacMan.actions(self, board))

    # Returns true if the game is over (pac-man is eaten by a ghost or has eaten all the dots) or false if not over
    def gameOver(self, board):
        return (self.lives == 0) | (board.dotsLeft == 0)

    # Returns the amount of lives Pac Man has left
    def getLives(self):
        return self.lives

    # Creates a tuple where the board (2 dimensional list) is the first element, and the move is the second element.
    # This is later used as the key to the Q dictionary
    def boardMoveTuple(self, board, move):
        boardTuple = copy.deepcopy(board.board)
        for i in range(0, len(boardTuple)):
            boardTuple[i] = tuple(board.board[i])
        boardTuple = tuple(boardTuple)
        return (boardTuple, move)

    # Returns the move that is the best available from the trained Q table
    def useReinforcementTable(self, board, Q):
        moves = PacMan.actions(self, board)
        bestValue = -65535
        bestMove = ""
        for move in moves:
            value = Q.get(PacMan.boardMoveTuple(self, board, move), 0)
            if value > bestValue:
                bestValue = value
                bestMove = move
        return bestMove

    # Choose a random move if random.uniform() < epsilon, otherwise, choose the move that has the least total moves to eat all dots
    def epsilonGreedy(self, epsilon, Q, state):
        moves = PacMan.actions(self, state)
        if np.random.uniform() < epsilon:
            # Make a random move
            return random.choice(moves)
        else:# #Choose the move with the highest score
            Qs = np.array([Q.get(PacMan.boardMoveTuple(self, state, m), 0) for m in moves])
            return moves[np.argmax(Qs)]

    def trainQ(self, board, nRepetitions, learningRate, epsilonDecayFactor, ghostsAvailable, intelligenceLevel, verbose=False):
        maxGames = nRepetitions
        rho = learningRate
        epsilonDecayRate = epsilonDecayFactor
        epsilon = 1.0
        Q = {}
        scores = []

        for nGames in range(maxGames):
            if verbose:
                print("Game:", nGames, "; Starting game.")
            epsilon *= epsilonDecayRate
            step = 0
            state = copy.deepcopy(board)
            copySelf = copy.deepcopy(self)
            ghosts = []
            score = 0
            done = False

            while not done and not copySelf.gameOver(state):
                dead = False
                copyGhosts = copy.deepcopy(ghostsAvailable)
                step += 1
                copyState = copy.deepcopy(state)
                move = PacMan.epsilonGreedy(copySelf, epsilon, Q, copyState)

                _, ghosts, copySelf, stateNew, score, dead = PlayGame.runSingleTurn(step, ghosts, copyGhosts, intelligenceLevel, copySelf, copyState, score, dead, move)
                # Full return: turn, ghosts, p, board, score, dead

                #Initial value
                if PacMan.boardMoveTuple(copySelf, state, move) not in Q:
                    Q[PacMan.boardMoveTuple(copySelf, state, move)] = 0  # initial Q value for new state,move

                if stateNew.dotsLeft < state.dotsLeft:
                    #Pacman ate a dot. Medium positive reinforcement
                    Q[PacMan.boardMoveTuple(copySelf, state, move)] += 3
                else:
                    #Pacman did not eat a dot. Small negative reinforcement
                    Q[PacMan.boardMoveTuple(copySelf, state, move)] += -1
                if dead:
                    #Pacman lost a life. Large negative reinforcement
                    Q[PacMan.boardMoveTuple(copySelf, state, move)] = -10

                if step > 1:
                    Q[PacMan.boardMoveTuple(copySelf, stateOld, moveOld)] += rho * (Q[PacMan.boardMoveTuple(copySelf, state, move)] - Q[PacMan.boardMoveTuple(copySelf, stateOld, moveOld)])

                stateOld, moveOld, scoreOld = state, move, score
                state = stateNew
            if verbose:
                if copySelf.lives > 0:
                    print("Pacman Won!")
                else:
                    print("Pacman Lost!")
            scores.append(score)
        return Q, scores