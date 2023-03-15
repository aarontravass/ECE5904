from flask import Flask, Response, request
import os
from dotenv import load_dotenv
import json
from flask_cors import CORS
import src.game.util as game_util

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/v1/game/new")
def init_game():
    res = game_util.init();
    return Response(response=json.dumps(res), status=res.get('statusCode'), mimetype='application/json')


if __name__ == "__main__":
    port = os.getenv('PORT')
    host = os.getenv('HOST')
    app.run(host=host, port=port, debug=True)
