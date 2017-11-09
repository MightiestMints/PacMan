import PacMan as P
import Ghost as G

# Creates Pac Man and starts the game. State is passed in as a parameter
# Right now the state is advancing a turn only after a move is selected. This will change when Pac Man gets his smarts
def startGame(state):
    p = P.PacMan(state)
    while not p.gameOver():
        print("Lives:", p.getLives(), "\tDots left:", p.dotsLeft, "\tLocation:", p.location)
        p.printState(state)
        print("\nActions available:", p.actions(state))
        state = p.takeAction(state, input("Action: "))
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    if p.lives == 0:
        print("You died")
    else: print("You ate all the dots with", p.getLives(), "left!")

if __name__ == "__main__":

    # Really basic state to start with
    state = [["==========="],
             ["|G        |"],
             ["| === === |"],
             ["| | | | | |"],
             ["| === === |"],
             ["|........P|"],
             ["==========="]]

    startGame(state)