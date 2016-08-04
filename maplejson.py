from flask import jsonify
from flask import Flask
from maplerank import get_rank

app = Flask(__name__)


@app.route("/")
def info():
    return "<h1>MapleStoryRankJsonService</h1><pre>/search/&lt;in_game_name&gt;</pre>"


@app.route("/search/<ign>")
def search(ign):
    try:
        data = get_rank(ign)
        if data is not None:
            return jsonify(data)
        else:
            return jsonify({"error": "The IGN you searched for was not found."})
    except:
        return jsonify({"error": "There was connection error to the server."})

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
