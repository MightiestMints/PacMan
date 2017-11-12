import PacMan as P
import Ghost as G
import Dot as d

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

def ghostSpawnPt(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 'G':
                return i, j
    # If it didn't find the location
    print("Could not find ghost spawn point in calculateLocation")
    return None

def pacManSpawnPoint(state):
    spawnLoc = None
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 'P':
                spawnLoc = i, j
    return spawnLoc

# Creates Pac Man and starts the game. State is passed in as a parameter
# Right now the state is advancing a turn only after a move is selected. This will change when Pac Man gets his smarts
# Currently spawns a Ghost after the first turn
def startGame(state):
    # Current Score of the game stored as an Integer
    score = 0
    p = P.PacMan(state, pacManSpawnPoint(state))
    ghostSpawn = ghostSpawnPt(state)
    ghosts = []
    dots = getDots(state)
    turn = 1
    while not p.gameOver():
        print("Lives:", p.getLives(), "\tDots left:", p.dotsLeft, "\tLocation:", p.location, "\tTurn:", turn, "\tScore:", score)
        # Number of dots remaining and lives at the beginning of the turn. This is used in score calculation.
        beginNumDots = p.dotsLeft
        beginNumLives = p.getLives()
        if turn is 5:
            ghosts.append(G.Ghost(state, ghostSpawn))
            turn = 0
        p.printState(state)
        print("\nActions available:", p.actions(state))
        for ghost in ghosts:
            state = ghost.randomMove(state)
        state = p.takeAction(state, input("Action: "))
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
    if p.lives == 0:
        print("You died")
    else: print("You ate all the dots with", p.getLives(), "lives left!")

if __name__ == "__main__":

    # Really basic state to start with
    state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', 'G', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', '.', '.', '.', '.', '.', '.', '.', '.', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]

    startGame(state)