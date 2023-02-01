from multiprocessing import Pool
# This is a sample Python script.
from chess import Board, Move 
from chess_game.player import MiniMaxPlayer
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chess_game.board import game_over, check_tie, check_win, eval_board_state
from chess_game.config import BOARD_SCORES
from time import perf_counter


def main(depth: int):
    # Use a breakpoint in the code line below to debug your script.
    board = Board()
    choice = True;

    while(1):
        print(board)
        if(choice):
            print("Input Move")
            move = input()
            board.push(Move.from_uci(move))
        else:
            pool = Pool(2)
            print("Bot move")
            bot1 = MiniMaxPlayer(False, 2)
            bot2 = MiniMaxPlayer(False, 4)
            time1 = perf_counter()
            r1=pool.apply(bot1.move, args=(board,))
            print("Time for Depth 2 is ", perf_counter() - time1)
            time1 = perf_counter()
            r2=pool.apply(bot2.move, args=(board,))
            print("Time for Depth 4 is ", perf_counter() - time1)

            print(r1)
            print(r2)
            best_move = r1
            board.push(Move.from_uci(best_move))
            pool.close()
        choice = not choice
        if game_over(board, claim_draw=True):
            break

    if check_tie(board, claim_draw=True):
        result = -1
    else:
        result = int(check_win(board, True))
    print(result)


if __name__ == '__main__':
    main(3)

