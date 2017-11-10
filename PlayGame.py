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

# Creates Pac Man and starts the game. State is passed in as a parameter
# Right now the state is advancing a turn only after a move is selected. This will change when Pac Man gets his smarts
# Currently spawns a Ghost after the first turn
def startGame(state):
    p = P.PacMan(state)
    ghosts = []
    dots = getDots(state)
    turn = 1
    while not p.gameOver():
        print("Lives:", p.getLives(), "\tDots left:", p.dotsLeft, "\tLocation:", p.location, "\tTurn:", turn)
        if turn is 5:
            ghosts.append(G.Ghost(state))
            turn = 0
        p.printState(state)
        print("\nActions available:", p.actions(state))
        state = p.takeAction(state, input("Action: "))
        for ghost in ghosts:
            state = ghost.randomMove(state)
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