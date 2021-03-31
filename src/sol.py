import argparse
from parserTools import *
from game import TaquinGame
from utils import *

def solTaquin(args):
    movements = ['right', 'up','left','down'];
    f_back_movements = ['left', 'down','right','up'];
    init_board = init_Board(args.file);
    board = deepcopy(init_board.board);
    scores = [0, 0, 0 , 0];
    closed_list = [];
	#while (min([i for i in scores if i >= 0]) != 0):
    i = 0;
    back_movements = [""];
    solution = [];
    stop = 0;
    while (stop != 1):
        scores = [];
        for move in movements:
            score = init_board.test_move(move, True);
            if (score != -1):
                scores.append(score.score);
            else:
                scores.append(-1);
        positive_score = False;
        for k in scores:
            if (k >= 0):
                positive_score = True;
                #si tout les scores sont à -1:
                #si len(back_movements) > 1:
                    #on utilise le back_movements[-1] pour le prochain taquin
                    #on enleve le dernier element a back_movements
                #else:
                    #taquin impossible
        if positive_score == True:
            i_mov = scores.index(min([j for j in scores if j >= 0]));
            init_board.test_move(movements[i_mov], False);
            solution.append(movements[i_mov]);
            back_movements.append(f_back_movements[i_mov]);
            stop = min([j for j in scores if j > 0])
            i = i + 1;
        else:
            if len(back_movements) > 1:
                init_board.test_move(back_movements[-1], False);
                solution.pop();
                back_movements.pop();
                i = i - 1;
            else:
                error("Taquin impossible");
        print("Mouvements = ", len(back_movements) - 1);
        init_board.printBoard();
    return solution;