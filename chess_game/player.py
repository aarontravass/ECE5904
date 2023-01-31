import logging as log

from random import choice
from math import inf
from time import time
from itertools import zip_longest
from queue import Queue
from chess import Board, Move
# from copy import deepcopy

from abc import ABC, abstractmethod

try:
    from board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from config import BOARD_SCORES, END_SCORES, PIECES
except ModuleNotFoundError:
    from .board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from .config import BOARD_SCORES, END_SCORES, PIECES




class Player(ABC):
    def __init__(self, player: bool, solver: str=None):
        self.player = player
        self.solver = solver

    @abstractmethod
    def move(self):
        pass



class MiniMaxPlayer(Player):
    def __init__(self, player, queue: Queue, id: int, depth=5,  verbose=False):
        super().__init__(player, "minimax")
        # TODO: problem for game func with accept classes - how to change depth
        self.depth = depth
        self.verbose = verbose
        self.queue = queue
        self.id = id

    def _minimax(self, board: Board, player: bool, depth: int, alpha: float=-inf, beta: float=inf) -> str:
        # base case
        if depth == 0 or game_over(board):
            return [game_score(board, self.player, END_SCORES, BOARD_SCORES), None]

        # first move for white
        if len(board.move_stack) == 0:
            white_opening = choice(("e2e4", "d2d4", "c2c4", "g1f3"))
            return white_opening

        moves = sorted_moves(board)

        if board.turn == player:
            maxScore, bestMove = -inf, None

            for move, piece in moves:
                test_board = board.copy()
                test_board.push(move)

                score = self._minimax(test_board, not player, depth - 1, alpha, beta)
                
                

                alpha = max(alpha, score[0])
                if beta <= alpha:
                    break

                if score[0] >= maxScore:
                    maxScore = score[0]
                    bestMove = move

            return [maxScore, bestMove]
        else:
            minScore, bestMove = inf, None

            for move, piece in moves:
                test_board = board.copy()
                test_board.push(move)

                score = self._minimax(test_board, player, depth - 1, alpha, beta)
                
                beta = min(beta, score[0])
                if beta <= alpha:
                    break

                if score[0] <= minScore:
                    minScore = score[0]
                    bestMove = move

            return [minScore, bestMove]

    def move(self, board: Board) -> str:
        best_move = self._minimax(board, self.player, self.depth)
        self.queue.put({ self.id:best_move[1].uci()})
    
    


if __name__ == "__main__":
    test_board = Board()
    