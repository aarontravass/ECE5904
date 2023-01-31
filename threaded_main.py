from threading import Thread
from queue import Queue
# This is a sample Python script.
from chess import Board, Move 
from chess_game.player import MiniMaxPlayer
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chess_game.board import game_over, check_tie, check_win, eval_board_state
from chess_game.config import BOARD_SCORES



def main(depth: int):
    # Use a breakpoint in the code line below to debug your script.
    board = Board()
    choice = True;
    
    while(1):
        print(board)
        queue = Queue()
        if(choice):
            print("Input Move")
            move = input()
            board.push(Move.from_uci(move))
        else:
            print("Bot move")
            bot1 = MiniMaxPlayer(False, queue, 1, 3)
            bot2 = MiniMaxPlayer(False, queue, 1, 5)
            t1 = Thread(target=bot1.move, args=(board))
            t2 = Thread(target=bot2.move, args=(board))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            val1 = queue.get()
            val2 = queue.get()
            print(val1)
            print(val2)
            best_move = val1[1]
            board.push(Move.from_uci(best_move))
        choice = not choice
        if game_over(board, claim_draw=True):
            break

    if check_tie(board, claim_draw=True):
        result = -1
    else:
        result = int(check_win(board, True))
    print(result)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(3)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
