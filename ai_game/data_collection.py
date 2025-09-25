import csv
import os
from datetime import datetime
from ai_game.ai_pieces import PieceType


'''I'm the collector baby'''

class DataCollector:
    def __init__(self, file_name='game_data.csv'):
        self.file_name = file_name
        self.fieldnames = [
            'game_state', 'action', 'outcome', 'board_evaluation', 'reward', 'winner', 
            'loser', 'episode', 'turn', 'q_value', 'q_value_change', 'exploration', 'current_turn', 'cumulative_reward'
        ]
        self.ensure_csv_file()

    def ensure_csv_file(self):
        try:
            with open(self.file_name, mode='x', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
        except FileExistsError:
            pass

    def log_data(self, game_state, action, outcome, board_evaluation, reward, winner=None, loser=None, episode=None, turn=None, q_value=None, q_value_change=None, exploration=None, current_turn=None, cumulative_reward=None):
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
            'current_turn': current_turn,
            'cumulative_reward': cumulative_reward
        }
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(data)

    def log_game_end(self, episode):
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['---', 'End of Game', '---', '', '', '', '', '', episode, '', '', '', '', ''])
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

if __name__ == "__main__":
    from ai_game.ai_logic import Game
    game = Game()
    data_collector = DataCollector()

    # Example game state and action
    game_state = data_collector.serialize_game_state(game)
    action = data_collector.serialize_action('place_pawn', {'row': 0, 'col': 1})
    outcome = 'win'

    data_collector.log_data(game_state, action, outcome)
    data_collector.log_game_end()