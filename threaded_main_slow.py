from multiprocessing import Pool
# This is a sample Python script.
from chess import Board, Move 
from chess_game.player import MiniMaxPlayer, HumanPlayer, Node, MonteCarlo
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chess_game.board import game_over, check_tie, check_win, eval_board_state
from chess_game.config import BOARD_SCORES
from time import perf_counter
import secrets

m2=0
mcts=0
m4=0
m2_avg=0
mcts_avg=0
m4_avg = 0
random_time = False
def main():
    # Use a breakpoint in the code line below to debug your script.
    board = Board()
    choice = True;
    start = True
    global m2, mcts, m2_avg, mcts_avg, m4, m4_avg
    count=0
    while(1):
        if(choice):
            move = None
            if(start):
                move = secrets.SystemRandom().choicefn(("e2e4", "d2d4", "c2c4", "g1f3"))
                start = False
            else:
                bot1 = MiniMaxPlayer(False, 2)
                move = bot1.move(board, -1)[0]
            #print("Player Move", move)
            board.push(Move.from_uci(move))
        else:
            count+=1
            pool = Pool(3)
            #print("Bot move")
            cut_of_time = secrets.SystemRandom().randint(0, 30) if random_time else -1
            bot1 = MiniMaxPlayer(False, 2)
            bot2 = MiniMaxPlayer(False, 4)
            r1=pool.apply(bot1.move, args=(board, cut_of_time))
            r2=pool.apply(bot2.move, args=(board, cut_of_time))
            r3 = pool.apply(mcts_main, args=(board, cut_of_time))
            moves = []
            if (r1[0] is not None):
                moves.append((r1[0], round(r1[1], 2)))

            if (r3[0] is not None):
                moves.append((r3[0], round(r3[1], 2)))

            if (r2[0] is not None):
                moves.append((r2[0], round(r2[1], 2)))

            if (random_time):
                moves = [moves.pop()]

            best_move = moves
            
            #print("m2 mcts m4")
            if not random_time:
                m2+=moves[0][1]
                mcts+= moves[1][1]
                m4+=moves[2][1]
            else:
                print(cut_of_time, best_move[0][0], best_move[0][1])
            board.push(Move.from_uci(best_move[1][0]))
            pool.close()
        
        if game_over(board, claim_draw=True):
            break
        choice = not choice

    if check_tie(board, claim_draw=True):
        result = -1
    else:
        result = int(check_win(board, choice))
    # print(result)
    m2/=float(count)
    mcts/=float(count)
    m4/=float(count)
    print(m2, mcts, m4)
    m2_avg += m2
    mcts_avg += mcts
    m4_avg += m4

def mcts_main(board: Board, cut_of_time: int) -> None:
    temp = board.copy()
    root = Node()
    root.board = temp
    child = MonteCarlo()
    ans = child.main(root, cut_of_time, 5)
    return ans

    

if __name__ == '__main__':
    itr = 10
    for i in range(itr):
        print("starting itr ", i+1)
        main()
        print("completed itr ", i+1)
    print(m2_avg/float(itr), mcts_avg/float(itr), m4_avg/float(itr))

