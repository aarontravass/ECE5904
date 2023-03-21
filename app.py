from flask import Flask, Response, request
import os
from dotenv import load_dotenv
import json
from flask_cors import CORS
import src.game.util as game_util

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def init():
    return "Hello World"

@app.route("/v1/game/new", methods = ['GET'])
def init_game():
    print("hello")
    res = game_util.init();
    return Response(
        response=json.dumps(res), 
        status=res.get('statusCode'), 
        mimetype='application/json'
    )


@app.route("/v1/game/player/move", methods = ['PUT'])
def playermove():
    body = request.json
    res = game_util.makeMove(body.get('client_id'), body.get('move'));
    return Response(
        response=json.dumps(res), 
        status=res.get('statusCode'), 
        mimetype='application/json'
    )

@app.route("/v1/game/bot/moves/fetch", methods = ['POST'])
def botmovefetch():
    body = request.json
    res = game_util.callBotMove(body.get('client_id'));
    return Response(
        response=json.dumps(res), 
        status=res.get('statusCode'), 
        mimetype='application/json'
    )

@app.route("/v1/game/bot/move", methods = ['PUT'])
def botmove():
    body = request.json
    res = game_util.chooseBotMove(body.get('client_id'), body.get('move'));
    return Response(
        response=json.dumps(res), 
        status=res.get('statusCode'), 
        mimetype='application/json'
    )


if __name__ == "__main__":
    port = os.getenv('PORT')
    host = os.getenv('HOST')
    app.run(host=host, port=port, debug=True)
