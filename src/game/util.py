import os, binascii
import database.handler as dbhandler
from chess import Board
instanceDB = mongo.getDb().get_database('public')
game = instanceDB['game']

def init() -> dict:
    client_id = binascii.b2a_hex(os.urandom(15))
    board = Board()
    data = {
        'users_turn': True,
        'fen': str(board.fen()),
        'client_id': client_id
    }
    game.insert(data)
    response = {
        'statusCode': 201,
        'status': True,
        'data': data
    }
    return response
