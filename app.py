from flask import Flask, render_template, jsonify, request
from game_logic import Game

app = Flask(__name__)
game = Game()

@app.route('/')
def index():
    if len(game.players) < 4:
        return render_template('redirect.html')  # redirección si no hay jugadores
    return render_template('index.html')


@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.json
    game.add_player(data['name'], data['icon'])
    return jsonify({'status': 'ok'})

@app.route('/roll', methods=['POST'])
def roll():
    result = game.move_player()
    return jsonify(result)

@app.route('/state')
def state():
    return jsonify(game.get_state())

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    for p in data['players']:
        game.add_player(p['name'], p['icon'])
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)

