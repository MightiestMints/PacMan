import PacMan as P
import GameBoard as B
import Ghost as G
import PlayGame as PG


def run(state, numGhosts, intelligenceLevel, IDS, verbose):

    # Run with Q Table
    if not IDS:
        board = B.GameBoard(state)
        p = P.PacMan(board.pacManSpawnPt)
        ghosts = []
        for i in range(numGhosts):
            ghosts.append(G.Ghost(board.ghostSpawnPt))
        if verbose: print("\tRunning PacMan with Q Table\n\tTraining Q Table...")
        Q, scores = p.trainQ(board, 30, 0.5, 0.7, ghosts, intelligenceLevel)
        if verbose: print("\tDone!\n\tRunning game...")
        results = PG.startGame(board, p, ghosts, Q, intelligenceLevel, False, False)
        if verbose: print("\tDone!")
        ghostInfo = "[" + str(numGhosts) + ", " + str(intelligenceLevel) + "]"
        print("\t", ghostInfo, "Q Table Results:\t\tTurns:", results[0], "\tScore:", results[1], "\tLives left:", results[2], "\tDots left:", results[3])
    # Run with Pacman IDS
    else:
        avgResults = [0, 0, 0, 0, 0]
        if verbose: print("\tRunning PacMan with IDS 30 times")
        for i in range(30):
            board = B.GameBoard(state)
            p = P.PacMan(board.pacManSpawnPt)
            ghosts = []
            for j in range(numGhosts):
                ghosts.append(G.Ghost(board.ghostSpawnPt))
            Q = []
            results = PG.startGame(board, p, ghosts, Q, intelligenceLevel, True, False)
            if verbose: print("\tIDS", (i + 1), "results:\t\tTurns:", results[0], "\tScore:", results[1], "\tLives left:",
                              results[2], "\tMoves explored:", results[3], "\tDots left:", results[4])
            for j in range(len(results)):
                avgResults[j] += results[j]
        if verbose: print("\tDone!")
        for i in range(len(avgResults)):
            avgResults[i] = int(avgResults[i] / 30)
        ghostInfo = "[" + str(numGhosts) + ", " + str(intelligenceLevel) + "]"
        print("\t", ghostInfo, "IDS 30-average results:\t\tTurns:", avgResults[0], "\tScore:", avgResults[1], "\tLives left:", avgResults[2],
              "\tDots left:", avgResults[3])

def printState(state):
    for row in state:
        for item in row:
            print(item, end='')
        print()
    print()

def board1(numGhosts, intelligenceLevel, IDS, verbose):
    state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', ' ', ' ', ' ', ' ', 'G', ' ', ' ', ' ', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', '.', '.', '.', '.', '.', '.', '.', '.', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]
    if verbose:
        printState(state)
    run(state, numGhosts, intelligenceLevel, IDS, False)
    return state

def board2(numGhosts, intelligenceLevel, IDS, verbose):
    state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', '.', ' ', ' ', ' ', 'G', ' ', ' ', ' ', '.', '|'],
             ['|', '.', '=', '=', '=', ' ', '=', '=', '=', '.', '|'],
             ['|', '.', '|', ' ', '|', ' ', '|', ' ', '|', '.', '|'],
             ['|', '.', '=', '=', '=', ' ', '=', '=', '=', '.', '|'],
             ['|', '.', '.', '.', '.', '.', '.', '.', '.', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]

    if verbose:
        printState(state)
    run(state, numGhosts, intelligenceLevel, IDS, False)
    return state

def board3(numGhosts, intelligenceLevel, IDS, verbose):
    state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', '.', ' ', '.', ' ', 'G', ' ', '.', ' ', '.', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', '.', '|', ' ', '|', '.', '|', ' ', '|', '.', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', '.', '|'],
             ['|', '.', ' ', '.', ' ', '.', ' ', '.', ' ', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]
    if verbose:
        printState(state)
    run(state, numGhosts, intelligenceLevel, IDS, False)
    return state

if __name__ == "__main__":

    print("\nFormat: [<number of ghosts>, <ghost intelligence level (1-3)>] <pacMan AI>  <turns>  <score>  <lives left>"
          "  <moves explored>  <dots left>\n\n")

    # print("Board 1:")
    # for i in range(1, 4):
    #     for j in range(1, 4):
    #         if i is 1 and j is 1:
    #             board1(i, j, True, True)
    #         else:
    #             board1(i, j, True, False)
    #         board1(i, j, False, False)
    #
    # print("Board 2:")
    # for i in range(1, 4):
    #     for j in range(1, 4):
    #         if i is 1 and j is 1:
    #             board2(i, j, True, True)
    #         else:
    #             board2(i, j, True, False)
    #         board2(i, j, False, False)
    #
    # print("Board 3:")
    # board3(1, 1, True, True)
    # board3(1, 1, False, False)
    # board3(1, 2, True, False)
    # board3(1, 2, False, False)
    # board3(1, 3, True, False)
    # board3(1, 3, False, False)

    # board3(2, 1, True, True)
    # board3(2, 1, False, False)
    # board3(2, 2, True, False)
    # board3(2, 2, False, False)
    # board3(2, 3, True, False)
    # board3(2, 3, False, False)
    # 
    # print("\nProgram exiting")


