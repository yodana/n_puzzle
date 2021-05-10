import argparse
from src.parserTools import *
from src.taquin import Taquin
from src.tree import Tree
from play import TaquinGame

def printBoard(board):
    print(' ------- ')
    for line in board:
        print(line)
    print(' ------- ')

def showSolution(moves, board, taquin):
    printBoard(board)
    for move in moves:
        board = taquin.move(move, board)
        printBoard(board)

def resolv(board, args):
    taquin = Taquin(board, args.heuristic)
    tree = Tree(taquin.getState(), args.time)
    while True:
        checkNode = tree.getBest()
        taquin.setState(checkNode)
        tree.close(checkNode)
        for child in taquin.getChildsStates():
            if taquin.isSolved(child['board']):
                showSolution(child['moves'], board, taquin)
                return tree.show(child)
            similar, index = tree.getByHash(child['hash'], "close")
            if similar is not None:
                if child['score'] < similar['score']:
                    tree.CLOSE.pop(index)
                    tree.open(child)
            else:
                tree.OPEN.append(child)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Must be a valid taquin file")
    parser.add_argument("-t", "--time", action="store_true", default=False, help="Visual on time")
    parser.add_argument("-v", "--view", action="store_true", default=False, help="enable visualizer")
    parser.add_argument("-f", "--heuristic", default='manhatan', help="chose the heuristic function (manhatan, euclide, best, inversion or perso)")
    args = parser.parse_args()
    if not getattr(args, 'file'):
        error('file expected')
    board = getBoard(args.file)
    solution = resolv(board, args)
    if args.view:
        TaquinGame(board, solution)