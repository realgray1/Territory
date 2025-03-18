import csv

class DataCollector:
    def __init__(self, file_name='game_data.csv'):
        self.file_name = file_name
        self.fieldnames = [
            'game_state', 'action', 'outcome', 'board_evaluation', 'reward', 'winner', 
            'loser', 'episode', 'turn', 'q_value', 'q_value_change', 'exploration', 'current_turn'
        ]
        self.ensure_csv_file()

    def ensure_csv_file(self):
        try:
            with open(self.file_name, mode='x', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
        except FileExistsError:
            pass

    def log_data(self, game_state, action, outcome, board_evaluation, reward, winner=None, loser=None, episode=None, turn=None, q_value=None, q_value_change=None, exploration=None, current_turn=None):
        data = {
            'game_state': game_state,
            'action': action,
            'outcome': outcome,
            'board_evaluation': board_evaluation,
            'reward': reward,
            'winner': winner,
            'loser': loser,
            'episode': episode,
            'turn': turn,
            'q_value': q_value,
            'q_value_change': q_value_change,
            'exploration': exploration,
            'current_turn': current_turn
        }
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(data)

    def log_game_end(self, episode):
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['---', 'End of Game', '---', '', '', '', '', '', episode, '', '', '', ''])  # Special row to mark the end of a game

    def serialize_game_state(self, game):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = game.board.get_piece_at(row, col)
                if piece:
                    pieces.append({
                        'type': piece.piece_type.name,
                        'color': piece.color,
                        'position': (row, col)
                    })
        return {
            'pieces': pieces,
            'action_points': game.action_points,
            'turn': game.turn
        }

    def serialize_action(self, action, parameters):
        return {
            'action': action,
            'parameters': parameters
        }

    def serialize_outcome(self, outcome):
        return outcome