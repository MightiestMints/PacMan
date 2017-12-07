import PacMan as P
import Ghost as G
import Dot as d
import GameBoard as Board
import copy as copy

# Scans through state and returns a list of Dot objects.
def getDots(state):
    dots = []
    for x, i in enumerate(state):
        for y, j in enumerate(state[x]):
            if j is '.':
                dots.append(d.Dot(x, y, False))
            if j is 'o':
                dots.append(d.Dot(x, y, True))
    return dots

def runSingleTurn(turn, ghosts, ghostsAvailable, intelligenceLevel, p, board, score, dead, move=""):
    beginNumDots = board.dotsLeft
    beginNumLives = p.getLives()
    if turn % 3 == 0 and len(ghosts) < len(ghostsAvailable):
        ghosts.append(ghostsAvailable[len(ghosts)])
    for ghost in ghosts:
        if intelligenceLevel is 0:
            state = ghost.randomMove(board)
        elif intelligenceLevel is 1:
            state = ghost.takeActionShortestDistance(board, p.location)
        elif intelligenceLevel is 2:
            state = ghost.intelligentMove(board, p.location)
        else:
            state = ghost.intelligentMove(board, p.location, maxDepth=8)

    # Check here first if ghost just killed Pacman
    for ghost in ghosts:
        if p.location == ghost.location:
            board.reset(p, ghosts)
            ghosts = []
            p.lives -= 1
            dead = True
    if not dead:
        if move == "":
            state = p.takeAction(board, input("Action: "))
        else:
            state = p.takeAction(board, move)

        #Now check again to see if Pacman just stupidly walked into a ghost spot
        for ghost in ghosts:
            if p.location == ghost.location:
                board.reset(p, ghosts)
                ghosts = []
                p.lives -= 1
                dead = True

    # Start of Score Calculation
    if score >= 1:
        score -= 1
    if beginNumDots > board.dotsLeft:
        score += 10
    if beginNumLives > p.getLives():
        if score > 100:
            score -= 100
        else:
            score = 0
    # End of Score Calculation
    turn += 1
    return turn, ghosts, p, board, score, dead

# Creates Pac Man and starts the game. State and Ghost objects are passed in as parameters
# Right now the state is advancing a turn only after a move is selected. This will change when Pac Man gets his smarts
# Currently spawns a ghost every 3 turns
def startGame(state, ghostsAvailable, intelligenceLevel=3):
    # Current Score of the game stored as an Integer
    board = Board.GameBoard(state)
    score = 0
    p = P.PacMan(board.pacManSpawnPt)
    ghostSpawn = board.ghostSpawnPt
    turn = 1
    dead = False
    ghosts = []

    #Q, scores = p.trainQ(board, 50, 0.5, 0.7, ghostsAvailable, intelligenceLevel)
    #print(scores)


    while not p.gameOver(board):
        beginGhosts = copy.deepcopy(ghostsAvailable)
        if dead:
            print("You died!")
            dead = False
        print("Lives:", p.getLives(), "\tDots left:", board.dotsLeft, "\tLocation:", p.location, "\tTurn:", turn, "\tScore:", score)
        # Number of dots remaining and lives at the beginning of the turn. This is used in score calculation.
        print(board, end='')
        print("\nActions available:", p.actions(board))
        # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        turn, ghosts, p, board, score, dead = runSingleTurn(turn, ghosts, beginGhosts, intelligenceLevel, p, board, score, dead)

    # Game over
    if p.lives == 0:
        print("Game over: You died!")
    else: print("Game over: You ate all the dots with", p.getLives(), "lives left!")

if __name__ == "__main__":

    # Really basic state to start with
    state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', ' ', ' ', ' ', ' ', 'G', ' ', ' ', ' ', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['t', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', 't'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', '.', '.', '.', '.', '.', '.', '.', '.', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]
    # Start game with above state and 2 ghosts
    board = Board.GameBoard(state)
    startGame(state, [G.Ghost(board.ghostSpawnPt)], 3)

    # Q, stepsToGoal = PacMan.trainQ(50, 0.5, 0.7, PacMan.actions(), PacMan.takeAction())
    # print(stepsToGoal)