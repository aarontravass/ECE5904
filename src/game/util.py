import binascii
import os
from chess import Board, Move, BLACK
import src.database.handler as mongo
from chess_game.board import game_over
from chess_game.player import HumanPlayer, Node, MonteCarlo, MiniMaxPlayer
from multiprocessing import Pool
instanceDB = mongo.getDb().get_database('public')
game = instanceDB.get_collection('game')


def init() -> dict:
    client_id = binascii.b2a_hex(os.urandom(15)).hex()
    board = Board()
    board.turn = BLACK
    data = {
        'users_turn': True,
        'fen': str(board.fen()),
        'client_id': client_id
    }
    game.insert_one(data)
    response = {
        'statusCode': 201,
        'status': True,
        'data': {
            'users_turn': True,
            'fen': str(board.fen()),
            'client_id': client_id
        }
    }
    print(data)
    return response


def makeMove(client_id: str, move: str) -> dict:
    game_res = game.find_one({'client_id': client_id})
    if game_res is None:
        response = {
            'statusCode': 404,
            'status': False,
            'data': None,
            'message': 'Game not found'
        }
        return response
    board = Board(game_res.get('fen'))
    if not game_res.get('users_turn'):
        response = {
            'statusCode': 401,
            'status': False,
            'data': None,
            'message': 'It is not your turn'
        }
        return response

    if game_over(board, claim_draw=True):
        response = {
            'statusCode': 200,
            'status': True,
            'data': {
                'game_over': True
            },
            'message': 'Game over'
        }
        return response
    h = HumanPlayer(False)
    #move = h.move(board)
    print(board.move_stack)
    board.push(Move.from_uci(move))
    print(board.move_stack)
    if game_over(board, claim_draw=True):
        response = {
            'statusCode': 200,
            'status': True,
            'data': {
                'game_over': True
            },
            'message': 'Game over'
        }
        return response
    data = {
        'users_turn': False,
        'fen': str(board.fen()),
    }
    newvalues = {"$set": data}
    game.update_one({'client_id': client_id}, newvalues)
    response = {
        'statusCode': 200,
        'status': True,
        'data': {
            'game_over': False,
            'users_turn': False,
            'fen': str(board.fen()),
            'client_id': client_id
        },
        'message': 'Game over'
    }
    return response


def callBotMove(client_id: str) -> dict:
    game_res = game.find_one({'client_id': client_id})
    if game_res is None:
        response = {
            'statusCode': 404,
            'status': False,
            'data': None,
            'message': 'Game not found'
        }
        return response
    print(game_res.get('fen'))
    board = Board(game_res.get('fen'))
    if game_res.get('users_turn'):
        response = {
            'statusCode': 401,
            'status': False,
            'data': None,
            'message': 'It is not your turn'
        }
        return response
    pool = Pool(3)
    print("Bot move")
    bot1 = MiniMaxPlayer(False, 2)
    bot2 = MiniMaxPlayer(False, 2)
    r1 = pool.apply(bot1.move, args=(board,))
    r2 = pool.apply(bot2.move, args=(board,))
    r3 = pool.apply(mcts_main, args=(board,))
    response = {
        'statusCode': 200,
        'status': True,
        'data': {
            0: {
                'player_name': 'Minimax',
                'move_gen': r1,
                'depth': 2
            },
            1: {
                'player_name': 'Minimax',
                'move_gen': r2,
                'depth': 4
            },
            2: {
                'player_name': 'Monte Carlo Tree Search',
                'move_gen': r3,
                'depth': None
            }
        },
        'message': None
    }
    return response


def chooseBotMove(client_id: str, move: str) -> dict:
    game_res = game.find_one({'client_id': client_id})
    if game_res is None:
        response = {
            'statusCode': 404,
            'status': False,
            'data': None,
            'message': 'Game not found'
        }
        return response
    board = Board(game_res.get('fen'))
    if game_res.get('users_turn'):
        response = {
            'statusCode': 401,
            'status': False,
            'data': None,
            'message': 'It is not your turn'
        }
        return response
    board.push(Move.from_uci(move))
    if game_over(board, claim_draw=True):
        response = {
            'statusCode': 200,
            'status': True,
            'data': {
                'game_over': True
            },
            'message': 'Game over'
        }
        return response
    data = {
        'users_turn': False,
        'fen': str(board.fen()),
    }
    newvalues = {"$set": data}
    game.update_one({'client_id': client_id}, newvalues)
    response = {
        'statusCode': 200,
        'status': True,
        'data': {
            'game_over': False,
            'users_turn': False,
            'fen': str(board.fen()),
            'client_id': client_id
        },
        'message': 'Game over'
    }
    return response


def mcts_main(board: Board) -> None:
    temp = board.copy()
    root = Node()
    root.board = temp
    child = MonteCarlo()
    ans = child.main(root, 5)
    return ans
