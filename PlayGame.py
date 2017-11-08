import PacMan as P
import Ghost as G

if __name__ == "__main__":

    # Really basic state to start with
    state = [["==========="],
             ["|G        |"],
             ["| === === |"],
             ["| | | | | |"],
             ["| === === |"],
             ["|o.......P|"],
             ["==========="]]

    # Create PacMan object
    p = P.PacMan(state)

    # Print state
    p.printState(state)

    # Game over?
    print("Game over?", p.gameOver())