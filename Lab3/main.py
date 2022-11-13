from sys import argv
from engine import GameEngine
import chess

if __name__ == '__main__':
    algo = argv[1].lower()
    if algo != "negamax" and algo != "negascout" and algo != "pvs":
        print("You need to set algorythm as a first argument (\"negamax\", \"negascout\" or \"pvs\")")
        exit()
    try:
        depth = int(argv[2])
    except:
        print("You need to set integer algorythm`s depth as a second argument")
        exit()
    color = argv[3].lower()
    if color != "white" and algo != "black":
        print("You need to set your starting color as a first argument (\"white\" or \"black\")")
        exit()
    print("Algorythm: ", algo)
    print("Depth: ", depth)
    print("You starting as ", color)

    game = GameEngine(chess.Board())
    game.start(algo, depth, color)