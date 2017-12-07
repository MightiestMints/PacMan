import copy as copy
import random
import numpy as np
import PlayGame as PlayGame

# Implements the learning algorithms that pac-man will use to maneuver through the game board, and avoid ghost/eat dots
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
        bestValue = 0
        bestMove = ""
        for move in moves:
            value = Q.get(PacMan.boardMoveTuple(self, board, move), 0)
            if value > bestValue:
                bestValue = value
                bestMove = move
        board = PacMan.takeAction(self, board, bestMove)
        return board

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
                # if verbose:
                #     print(state,end='')
                step += 1
                copyState = copy.deepcopy(state)
                move = PacMan.epsilonGreedy(copySelf, epsilon, Q, copyState)

                # Need only 3 return values:
                # 1. ghosts, because we need to keep passing in the array of ghosts so that they can make moves
                # 2. self, because we need to update PacMan object values
                # 3. stateNew, because we have a new board state
                _, ghosts, copySelf, stateNew, score, dead = PlayGame.runSingleTurn(step, ghosts, copyGhosts, intelligenceLevel, copySelf, copyState, score, dead, move)
                # Full return: turn, ghosts, p, board, score, dead

                #Initial value
                if PacMan.boardMoveTuple(copySelf, copyState, move) not in Q:
                    Q[PacMan.boardMoveTuple(copySelf, copyState, move)] = 0  # initial Q value for new state,move

                if stateNew.dotsLeft == 0:
                    # Pacman won. Big positive reinforcement
                    Q[PacMan.boardMoveTuple(copySelf, copyState, move)] += rho * (5 + Q[PacMan.boardMoveTuple(copySelf, copyState, move)])
                    if verbose:
                        print("Game:", nGames, "; Pacman won!")
                    done = True
                else:
                    if stateNew.dotsLeft < state.dotsLeft:
                        #Pacman ate a dot. Small positive reinforcement
                        Q[PacMan.boardMoveTuple(copySelf, copyState, move)] += rho * (1 - Q[PacMan.boardMoveTuple(copySelf, copyState, move)])
                    if dead == True:
                        #Pacman lost a life. Small negative reinforcement
                        Q[PacMan.boardMoveTuple(copySelf, copyState, move)] += rho * (-1 - Q[PacMan.boardMoveTuple(copySelf, copyState, move)])
                    if copySelf.lives == 0:
                        # Pacman lost. Big negative reinforcement
                        Q[PacMan.boardMoveTuple(copySelf, copyState, move)] += rho * (-5 - Q[PacMan.boardMoveTuple(copySelf, copyState, move)])
                        if verbose:
                            print("Game:", nGames, "; Pacman ran out of lives. Starting new game...")
                        score = 0
                        done = True

                if step > 1:
                    Q[PacMan.boardMoveTuple(copySelf, stateOld, moveOld)] += rho * (Q[PacMan.boardMoveTuple(copySelf, copyState, move)] - Q[PacMan.boardMoveTuple(copySelf, stateOld, moveOld)])

                stateOld, moveOld, scoreOld = copyState, move, score
                state = stateNew
            scores.append(score)
        return Q, scores