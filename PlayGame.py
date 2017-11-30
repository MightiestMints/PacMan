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




# Creates Pac Man and starts the game. State and Ghost objects are passed in as parameters
# Right now the state is advancing a turn only after a move is selected. This will change when Pac Man gets his smarts
# Currently spawns a ghost every 3 turns
def startGame(state, ghostsAvailable):
    # Current Score of the game stored as an Integer
    board = Board.GameBoard(state)
    score = 0
    p = P.PacMan(state, board.pacManSpawnPt)
    ghostSpawn = board.ghostSpawnPt
    turn = 1
    dead = False
    ghosts = []
    while not p.gameOver():
        if(dead):
            print("You died!")
            dead = False
        print("Lives:", p.getLives(), "\tDots left:", p.dotsLeft, "\tLocation:", p.location, "\tTurn:", turn, "\tScore:", score)
        # Number of dots remaining and lives at the beginning of the turn. This is used in score calculation.
        beginNumDots = p.dotsLeft
        beginNumLives = p.getLives()
        if turn % 3 == 0 and len(ghosts) < len(ghostsAvailable):
            ghosts.append(ghostsAvailable[len(ghosts)])
        p.printState(state)
        print("\nActions available:", p.actions(state))
        for ghost in ghosts:
            #state = ghost.intelligentMove(state, p.location)
            state = ghost.takeActionShortestDistance(state, p.location)
            #state = ghost.randomMove(state)
        state = p.takeAction(state, input("Action: "))
        # Respawn if Pac Man is killed
        for ghost in ghosts:
            if p.location == ghost.location:
                state[p.location[0]][p.location[1]] = ' '
                p.location = p.spawnPt()
                for g in ghosts:
                    state[g.location[0]][g.location[1]] = ' '
                ghosts = []
                p.lives -= 1
                state[p.location[0]][p.location[1]] = 'P'
                state[ghostSpawn[0]][ghostSpawn[1]] = 'G'
                dead = True
        # Start of Score Calculation
        if score >= 1 : score -= 1
        if beginNumDots > p.dotsLeft : score += 10
        if beginNumLives > p.getLives() :
            if score > 100:
                score -= 100
            else: score = 0
        # End of Score Calculation
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        turn += 1
    # Game over
    if p.lives == 0:
        print("Game over: You died!")
    else: print("Game over: You ate all the dots with", p.getLives(), "lives left!")

if __name__ == "__main__":

    # Really basic state to start with
    state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', 'G', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['t', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', 't'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', '.', '.', '.', '.', '.', '.', '.', '.', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]
    # Start game with above state and 2 ghosts
    board = Board.GameBoard(state)
    startGame(state, [G.Ghost(state, board.ghostSpawnPt), G.Ghost(state, board.ghostSpawnPt)])