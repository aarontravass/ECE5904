import logging as log

from random import choice
from math import inf, log, sqrt, e
from chess import Board, Move
# from copy import deepcopy

from abc import ABC, abstractmethod

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

class MonteCarlo(Player):
    def __init__(self, player):
        super().__init__(player, "mcts")
        # TODO: problem for game func with accept classes - how to change depth
        

    def ucb(node: Node) -> float:       
        ans = node.w_Score + 2*(sqrt(log(node.N+e+(10**-6))/(node.n+(10**-10))))
        return ans

    def selection(self, node: Node) -> Node:
        max_ucb = -inf
        selected_child = None
        for child in node.children:
            ucb_value = self.ucb(child)
            if ucb_value < max_ucb:
                max_ucb = ucb_value
                selected_child = child
        return selected_child
    
    def expand(self, node: Node) -> Node:
        if node.children.empty():
            return node
        return self.expand(self.selection(node))

    def rollout(self, node: Node):
        if(node.board.game_over()):
            if(node.board.result()=='1-0'):
                return (1, node)
            elif (node.board.result()=='0-1'):
                return (-1, node)
            else:
                return (0.5, node)
        
        all_moves = [node.state.san(i) for i in list(node.state.legal_moves)]
    
        for i in all_moves:
            tmp_state = Board(node.state.fen())
            tmp_state.push_san(i)
            child = Node()
            child.state = tmp_state
            child.parent = node
            node.children.add(child)
        rnd_state = choice(list(node.children))

        return self.rollout(rnd_state)

    def rollback(self, node: Node, reward):
        node.n+=1
        node.w_score+=reward
        while(node.parent!=None):
            node.N+=1
            node = node.parent
        return node

    def main(self, node: Node, iterations: int):
        all_moves = [node.board.san(i) for i in list(node.board.legal_moves)]
        map_state_move = dict()

        for i in all_moves:
            tmp_state = Board(node.board.fen())
            tmp_state.push_san(i)
            child = node()
            child.state = tmp_state
            child.parent = node
            node.children.add(child)
            map_state_move[child] = i
        while (iterations > 0):
            max_ucb = -inf
            sel_child = None
            for i in curr_node.children:
                tmp = self.ucb(i)
                if (tmp > max_ucb):
                    max_ucb = tmp
                    sel_child = i
            ex_child = self.expand(sel_child, 0)
            reward, state = self.rollout(ex_child)
            curr_node = self.rollback(state, reward)
            iterations -= 1
        mx = -inf
        selected_move = ''
        for i in (node.children):
            tmp = self.ucb(i)
            if (tmp > mx):
                mx = tmp
                selected_move = map_state_move[i]
        return selected_move


class MiniMaxPlayer(Player):
    def __init__(self, player, depth,  verbose=False):
        super().__init__(player, "minimax")
        # TODO: problem for game func with accept classes - how to change depth
        self.depth = depth
        self.verbose = verbose

    def _minimax(self, board: Board, player: bool, depth: int, alpha: float=-inf, beta: float=inf):
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
        return best_move[1].uci()
    
    


if __name__ == "__main__":
    test_board = Board()
    
