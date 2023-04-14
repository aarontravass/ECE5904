from multiprocessing import Pool
# This is a sample Python script.
from chess import Board, Move, parse_square
from chess_game.player import MiniMaxPlayer, HumanPlayer, Node, MonteCarlo
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chess_game.board import game_over, check_tie, check_win, eval_board_state
from chess_game.config import BOARD_SCORES
from time import perf_counter
from random import randint, choice as choicefn

found = False
random_time = False
def main():
    # Use a breakpoint in the code line below to debug your script.
    board = Board()
    choice = True;
    start = True
    global found
    
    i=0
    d= [
        [('c7c5', 0.03), ('f7f5', 8.73)],
        [('a7a6', 0.04), ('f5f4', 8.92)],
        [('d7d5', 0.05), ('a7a5', 7.25)],
        [('c8b7', 0.06), ('a8a7', 7.31)],
        [('d7d6', 0.06), ('h7h5', 6.64)],
        [('d8c8', 0.06), ('a5a4', 5.31)],
        [('a7c7', 0.08), ('a7a6', 5.71)],
        [('d8c8', 0.09), ('g7g6', 7.24)],
        [('d8b8', 0.1), ('a6d6', 5.98)],
        [('d8c8', 0.09), ('g8h6', 5.38)],
        [('e8d8', 0.01), ('e8d8', 5.84)]
    ]
    while(1):
        if(choice):
            move = None
            if(start):
                move = choicefn(("e2e4", "d2d4", "c2c4", "g1f3"))
                start = False
            else:
                bot1 = MiniMaxPlayer(True, 2)
                move = bot1.move(board, -1)[0]
            # print("Player Move", move)
            board.push(Move.from_uci(move))
        else:
            if(i>len(d)-1):
                break

            # if (r2[0] is not None):
            #     moves.append((r2[0], round(r2[1], 2)))

            
            moves = d[i]
            i+=1
            best_move = moves
           
            # print("bot moves", moves)
            # print(board.move_stack)
            if board.piece_at(parse_square(moves[0][0][0:2]))=='k' or board.piece_at(parse_square(moves[0][0][0:2]))=='K':
                
                print(board.fen())
                print(board.move_stack)
                return True
           
            board.push(Move.from_uci(best_move[1][0]))
           
        if game_over(board, claim_draw=True):
            break
        choice = not choice

    if check_tie(board, claim_draw=True):
        result = -1
    else:
        result = int(check_win(board, choice))
    #print(board)
    return False

def mcts_main(board: Board, cut_of_time: int) -> None:
    temp = board.copy()
    root = Node()
    root.board = temp
    child = MonteCarlo()
    ans = child.main(root, cut_of_time, 5)
    return ans

    

if __name__ == '__main__':
    # itr = 1
    # for i in range(itr):
    #     #print("starting itr ", i+1)
    #     main()
        #print("completed itr ", i+1)
    while(not found):
        try:
            if main():
                break
        except AssertionError:
            continue
    

