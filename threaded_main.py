from multiprocessing import Pool
# This is a sample Python script.
from chess import Board, Move 
from chess_game.player import MiniMaxPlayer, HumanPlayer, Node, MonteCarlo
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chess_game.board import game_over, check_tie, check_win, eval_board_state
from chess_game.config import BOARD_SCORES
from time import perf_counter
from random import randint, choice as choicefn


random_time = False
def main():
    # Use a breakpoint in the code line below to debug your script.
    board = Board()
    choice = True;
    start = True
    while(1):
        if(choice):
            move = None
            if(start):
                move = choicefn(("e2e4", "d2d4", "c2c4", "g1f3"))
                start = False
            else:
                bot1 = MiniMaxPlayer(False, 2)
                move = bot1.move(board, -1)[0]
            #print("Player Move", move)
            board.push(Move.from_uci(move))
        else:
            pool = Pool(3)
            #print("Bot move")
            cut_of_time = randint(0, 30) if random_time else -1
            bot1 = MiniMaxPlayer(False, 2)
            #bot2 = MiniMaxPlayer(False, 4)
            r1=pool.apply(bot1.move, args=(board, cut_of_time))
            #r2=pool.apply(bot2.move, args=(board, cut_of_time))
            r3 = pool.apply(mcts_main, args=(board, cut_of_time))
            moves = []
            if (r1[0] is not None):
                moves.append((r1[0], round(r1[1], 2)))

            if (r3[0] is not None):
                moves.append((r3[0], round(r3[1], 2)))

            # if (r2[0] is not None):
            #     moves.append((r2[0], round(r2[1], 2)))

            if (random_time):
                moves = [moves.pop()]

            best_move = moves
            if not random_time:
                print("m2 ", moves[0][1], " mcts ", moves[1][1])
            else:
                print(cut_of_time, best_move[0][0], best_move[0][1])
            board.push(Move.from_uci(best_move[1][0]))
            pool.close()
        choice = not choice
        if game_over(board, claim_draw=True):
            break

    if check_tie(board, claim_draw=True):
        result = -1
    else:
        result = int(check_win(board, True))
    print(result)

def mcts_main(board: Board, cut_of_time: int) -> None:
    temp = board.copy()
    root = Node()
    root.board = temp
    child = MonteCarlo()
    ans = child.main(root, cut_of_time, 5)
    return ans

    

if __name__ == '__main__':
    main()

