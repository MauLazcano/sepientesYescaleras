import random

class Game:
    def __init__(self):
        self.players = []
        self.positions = [0, 0, 0, 0]
        self.turn = 0
        self.snakes = {}
        self.ladders = {}
        self.generate_snakes_and_ladders()
        self.finished_order = []

    def generate_snakes_and_ladders(self):
        occupied = set()

        def biased_step():
            if random.random() < 0.7:
                return random.randint(5, 7)
            return random.randint(8, 12)

        while len(self.snakes) < 5:
            pos = random.randint(2, 99)
            if pos not in occupied:
                step = biased_step()
                if pos - step > 0:
                    self.snakes[pos] = step
                    occupied.add(pos)

        while len(self.ladders) < 5:
            pos = random.randint(2, 99)
            if pos not in occupied:
                step = biased_step()
                if pos + step <= 99:
                    self.ladders[pos] = step
                    occupied.add(pos)

    def add_player(self, name, icon):
        if len(self.players) < 4:
            self.players.append({'name': name, 'icon': icon})

    def roll_dice(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return d1, d2

    def move_player(self):
        if len(self.players) == 0:
            return {'error': 'No hay jugadores registrados.'}

        if len(self.finished_order) == len(self.players):
            return {'game_over': True, 'final_order': self.get_final_order()}

        d1, d2 = self.roll_dice()
        player_index = self.turn % len(self.players)

        # Si este jugador ya terminó, pasa el turno
        while player_index in self.finished_order:
            self.turn += 1
            player_index = self.turn % len(self.players)

        move = d1 + d2
        pos = self.positions[player_index] + move
        if pos >= 100:
            pos = 100

        if pos in self.snakes:
            pos -= self.snakes[pos]
        elif pos in self.ladders:
            pos += self.ladders[pos]

        self.positions[player_index] = pos

        if pos >= 100 and player_index not in self.finished_order:
            self.finished_order.append(player_index)

        self.turn += 1

        return {
            'dice': (d1, d2),
            'player': self.players[player_index]['name'],
            'position': pos,
            'player_index': player_index,
            'winner': pos >= 100,
            'game_over': len(self.finished_order) == len(self.players)
        }

    def get_final_order(self):
        return [self.players[i]['name'] for i in self.finished_order]


    def get_state(self):
        return {
            'players': self.players,
            'positions': self.positions,
            'snakes': self.snakes,
            'ladders': self.ladders,
            'turn': self.turn % len(self.players) if self.players else None
        }
