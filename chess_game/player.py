import logging as log
import sys
import os
from math import inf, log, sqrt, e
from chess import Board, Move
from time import time
from abc import ABC, abstractmethod
import secrets

sys.setrecursionlimit(15000)
try:
    from board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from config import BOARD_SCORES, END_SCORES, PIECES
except ModuleNotFoundError:
    from .board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from .config import BOARD_SCORES, END_SCORES, PIECES


class Node:
    def __init__(self) -> None:
        self.board = Board()
        self.children = set()
        self.parent = None
        self.N = 0
        self.w_Score = 0
        self.n = 0


class Player(ABC):
    def __init__(self, player: bool, solver: str):
        self.player = player
        self.solver = solver

    @abstractmethod
    def move(self):
        pass


class HumanPlayer(Player):
    def __init__(self, player: bool):
        super().__init__(player, "human")

    def _get_move(self, board: Board):
        uci = input(f"({turn_side(board)}) Choose move: ")

        # check legal uci move
        try:
            Move.from_uci(uci)
        except ValueError:
            uci = None
        return uci

    def move(self, board: Board) -> str:

        legal_moves = [move.uci() for move in board.legal_moves]

        move = self._get_move(board)

        while move is None:
            print("Invalid uci move! Try again.", )
            move = self._get_move(board)

        while (move not in legal_moves):
            print("Not a legal move! Avaliable moves:\n")
            move = self._get_move(board)

        return move


class MonteCarlo:
    def __init__(self):
        return

    def ucb(self, node: Node) -> float:
        ans = node.w_Score + 2 * (sqrt(log(node.N + e + (10 ** -6)) / (node.n + (10 ** -10))))
        return ans




    def expand(self, node: Node, white: int) -> Node:
        if len(node.children) == 0:
            return node
        max_ucb = -inf
        if(white):
            selected_child = None
            for child in node.children:
                ucb_value = self.ucb(child)
                if ucb_value > max_ucb:
                    max_ucb = ucb_value
                    selected_child = child
            return self.expand(selected_child, 0)
        else:
            min_ucb = inf
            selected_child = None
            for child in node.children:
                ucb_value = self.ucb(child)
                if ucb_value < min_ucb:
                    min_ucb = ucb_value
                    selected_child = child
            return self.expand(selected_child, 1)


    def rollout(self, node: Node):
        if node.board.is_game_over():
            if node.board.result() == '1-0':
                return (1, node)
            elif node.board.result() == '0-1':
                return (-1, node)
            else:
                return (0.5, node)

        all_moves = [node.board.san(i) for i in list(node.board.legal_moves)]

        for i in all_moves:
            tmp_state = Board(node.board.fen())
            tmp_state.push_san(i)
            child = Node()
            child.board = tmp_state
            child.parent = node
            node.children.add(child)
        # print(node.children)
        rnd_state = secrets.SystemRandom().choice(list(node.children))

        return self.rollout(rnd_state)

    def rollback(self, node: Node, reward):
        node.n += 1
        node.w_Score += reward
        while (node.parent != None):
            node.N += 1
            node = node.parent
        return node

    def main(self, node: Node, cut_of_time: int, iterations: int):
        t1 = time()
        #os.nice(-15)
        # set a low nice value to give it high priority
        original_board = node.board.copy()
        all_moves = [node.board.san(i) for i in list(node.board.legal_moves)]
        map_state_move = dict()
       
        for i in all_moves:
            tmp_state = Board(node.board.fen())
            tmp_state.push_san(i)
            child = Node()
            child.board = tmp_state
            child.parent = node
            node.children.add(child)
            map_state_move[child] = i
        while (iterations > 0):
            if(time() - t1 > cut_of_time and cut_of_time !=-1):
                return (None, None)
            min_ucb = inf
            sel_child = None
            for i in node.children:
                tmp = self.ucb(i)
                if (tmp < min_ucb):
                    min_ucb = tmp
                    sel_child = i
            ex_child = self.expand(sel_child, 1)
            reward, state = self.rollout(ex_child)
            node = self.rollback(state, reward)
            iterations -= 1
        mn = inf
        selected_move = ''
        for i in (node.children):
            tmp = self.ucb(i)
            if (tmp < mn):
                mn = tmp
                selected_move = map_state_move[i]
        #print("MCTS", selected_move, time() - t1)
        return (original_board.parse_san(selected_move).uci(), time() - t1)


class MiniMaxPlayer(Player):
    def __init__(self, player, depth, verbose=False):
        super().__init__(player, "minimax")
        # TODO: problem for game func with accept classes - how to change depth
        self.depth = depth
        self.verbose = verbose

    def _minimax(self, board: Board, player: bool, depth: int, t1: float, cut_of_time: int, alpha: float = -inf, beta: float = inf):
        # base case
        diff = time() - t1
        if(diff>cut_of_time and cut_of_time!=-1):
            return []

        if depth == 0 or game_over(board):
            return [game_score(board, self.player, END_SCORES, BOARD_SCORES), None]

        moves = sorted_moves(board)

        if board.turn == player:
            maxScore, bestMove = -inf, None

            for move, piece in moves:
                test_board = board.copy()
                test_board.push(move)

                score = self._minimax(test_board, not player, depth - 1, t1, cut_of_time, alpha, beta)
                if len(score) == 0:
                    return score
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

                score = self._minimax(test_board, player, depth - 1, t1, cut_of_time, alpha, beta)
                if len(score) == 0:
                    return score
                beta = min(beta, score[0])
                if beta <= alpha:
                    break

                if score[0] <= minScore:
                    minScore = score[0]
                    bestMove = move

            return [minScore, bestMove]

    def move(self, board: Board, cut_of_time: int):
        # os.nice(-15)
        # set a low nice value to give it high priority
        t1 = time()
        copy_board = board.copy()
        if((best_move := self._minimax(copy_board, self.player, self.depth, t1, cut_of_time)) == []):
            return (None, None)
        #print(best_move)
        return (best_move[1].uci(), time() - t1)


if __name__ == "__main__":
    test_board = Board()
