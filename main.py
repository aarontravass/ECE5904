# This is a sample Python script.
from chess import Board, Move 
from chess_game.player import MiniMaxPlayer
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chess_game.board import game_over, check_tie, check_win, eval_board_state
from chess_game.config import BOARD_SCORES



def main():
    # Use a breakpoint in the code line below to debug your script.
    board = Board()
    choice = True;
    bot = MiniMaxPlayer(player=False, verbose=False)
    while(1):
        print(board)
        if(choice):
            print("Input Move")
            move = input()
            board.push(Move.from_uci(move))
        else:
            print("Bot move")
            best_move = bot._minimax(board, False, 3)
            print(best_move[1].uci())
            board.push(Move.from_uci(best_move[1].uci()))
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
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
