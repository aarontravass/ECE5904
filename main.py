# This is a sample Python script.
from chess import Board, Move 
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
try:
    from board import game_over, check_tie, check_win, eval_board_state
    from config import BOARD_SCORES
except ModuleNotFoundError:
    from .board import game_over, check_tie, check_win, eval_board_state
    from .config import BOARD_SCORES
    

def main(name):
    # Use a breakpoint in the code line below to debug your script.
    board = Board()
    choice = True;
    while(1):
        if(choice):
            print("Input Move")
            move = input()
            board.push(Move.from_uci(move))
        else:

        if game_over(board, claim_draw=True):
            break





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
