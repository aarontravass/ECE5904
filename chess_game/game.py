
from bisect import insort_left
from chess import Board 

from itertools import count
from time import sleep, time
from random import choice

try:
    from board import game_over, check_tie, check_win, eval_board_state
    from config import BOARD_SCORES
except ModuleNotFoundError:
    from .board import game_over, check_tie, check_win, eval_board_state
    from .config import BOARD_SCORES


class Game:
    def __init__(self, board: Board):
        # for games with specific starting point
        if board:
            self.board = board
        else:
            self.board = Board()

    def _game(self, white_p, black_p, visual=False, pause=1):
        board = self.board.copy()
        result = None
        start_time = time()

        try:
            for i in count():
                if visual:
                   

                    white_score = eval_board_state(board, True, BOARD_SCORES)
                    black_score = eval_board_state(board, False, BOARD_SCORES)
                   
                    sleep(pause)

                if game_over(board, claim_draw=True):
                    break

                if board.turn:
                    move = white_p.move(board)
                else:
                    move = black_p.move(board)

                board.push_uci(move)
           
        except KeyboardInterrupt:
            print("Game stopped!")
            
        if check_tie(board, claim_draw=True):
            result = -1
        else:
            result = int(check_win(board, True))

       
        result_stat = {
            "white": white_p.solver, 
            "black": black_p.solver, 
            "FEN": board.fen(), 
            "last_move": board.peek(), 
            "moves_history": [move.uci() for move in board.move_stack],
            "moves": 0, "time": round(time() - start_time, 2),
            "result": result
            }
            
        return result_stat

    def start_game(self, p1_cls, p2_cls, visual=False, pause=1):
        goes_first = choice([True, False])
        
        if goes_first:
            result = self._game(p1_cls(True), p2_cls(False), visual, pause)
        else:
            result = self._game(p2_cls(True), p1_cls(False), visual, pause)
                
        return result

