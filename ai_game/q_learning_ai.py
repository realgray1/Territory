import os
import pickle
import random
import numpy as np

from ai_game.ai_pieces import PieceType, Piece
from ai_game.ai_logic import Game
from ai_game.data_collection import DataCollector
from ai_game.board_evaluation import evaluate_board


class QLearningAI:
    def __init__(self, game, player_name, alpha=0.1, gamma=0.9, epsilon=0.1, epsilon_decay=0.995, min_epsilon=0.01, episode=1):
        self.game = game
        self.data_collector = DataCollector()
        self.player_name = player_name
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Decay rate
        self.min_epsilon = min_epsilon  # Minimum value
        self.q_table = {}
        self.episode = episode
        self.turn_count = 0 
        self.previous_board_evaluation = evaluate_board(self.game)
        self.cumulative_reward = 0

    def load_q_table(self, file_path='qtable/q_table.pkl'):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.q_table = pickle.load(file)
        else:
            self.q_table = {}

    def save_q_table(self, file_path='qtable/q_table.pkl'):
        with open(file_path, 'wb') as file:
            pickle.dump(self.q_table, file)

    def get_state(self):
        # Need this to analyze board state
        return tuple([tuple(row) for row in self.game.board.board])

    def choose_action(self, state, valid_moves):
        '''USES THE Q TABLE TO FIND BEST MOVE'''
        exploration = False
        if not valid_moves:
            return None, exploration
        for move in valid_moves:
            pass

        if np.random.uniform(0, 1) < self.epsilon:
            # Exploration: Choose a random action
            action = random.choice(valid_moves)
            exploration = True
        else:
            # Exploitation: Choose the action with the highest Q-value
            q_values = [self.q_table.get((state, action), 0) for action in valid_moves]
            max_q = max(q_values)
            max_q_actions = [action for action, q in zip(valid_moves, q_values) if q == max_q]
            action = random.choice(max_q_actions)
        return action, exploration

    def update_q_value(self, state, action, reward, next_state, next_valid_moves, cumulative_reward):
        current_q = self.q_table.get((state, action), 0)
        if next_valid_moves:
            next_q = max([self.q_table.get((next_state, next_action), 0) for next_action in next_valid_moves])
        else:
            next_q = 0

        new_q = current_q + self.alpha * (cumulative_reward + self.gamma * next_q - current_q)
        q_value_change = abs(new_q - current_q)
        self.q_table[(state, action)] = new_q

        return q_value_change

    def calculate_reward(self, previous_evaluation, current_evaluation, action):
        '''checks how much the action changed the board state eval'''
        if action and action[0] == 'fire_turret':
            target_row, target_col = action[3], action[4]
            target_piece = self.game.board.get_piece_at(target_row, target_col)
            if target_piece and target_piece.piece_type == PieceType.KING:
                return 1000
        reward = abs(current_evaluation - previous_evaluation)
        return reward

    def log_action(self, action, outcome, exploration):
        state = self.get_state()
        previous_board_evaluation = evaluate_board(self.game)

        if action is not None:
            self.perform_action(action)

        current_board_evaluation = evaluate_board(self.game)
        reward = self.calculate_reward(previous_board_evaluation, current_board_evaluation, action)
        self.cumulative_reward += reward
        # Set reward to 500 if the outcome is a win
        if outcome == 'win':
            reward = 500

        q_value_change = self.update_q_value(state, action, reward, self.get_state(), self.find_valid_moves(), self.cumulative_reward)

        if action is not None:
            action_params = {'from': (action[1], action[2]) if action and len(action) > 2 else None}
            if action and len(action) > 4:
                action_params['to'] = (action[3], action[4])
            if action and action[0] == 'upgrade_pawn':
                action_params['to_type'] = action[3].name
        else:
            action_params = {'action': 'none', 'parameters': {}}

        winner = self.game.winner
        loser = "Player 2" if winner == "Player 1" else "Player 1" if winner else None

        self.data_collector.log_data(
            self.data_collector.serialize_game_state(self.game),
            self.data_collector.serialize_action(action[0], action_params) if action else {'action': 'none', 'parameters': {}},
            outcome, current_board_evaluation, reward, winner, loser, self.episode, self.turn_count,
            self.q_table.get((state, action), 0) if action else None, q_value_change, exploration, self.game.turn, self.cumulative_reward
        )



    def perform_action(self, action):
        '''performs the action :)'''
        color = self.get_current_color()
        if action[0] == 'place_pawn':
            self.game.board.place_piece(action[1], action[2], PieceType.PAWN, color)
            self.game.actions[color] -= 1
        elif action[0] == 'upgrade_pawn':
            self.game.board.board[action[1]][action[2]] = Piece(color, action[3])
            self.game.actions[color] -= 1
        elif action[0] == 'fire_turret':
            self.game.valid_targets = self.game.find_valid_targets_for_turret(action[1], action[2])
            self.game.fire_turret(action[1], action[2], action[3], action[4])


    def make_move(self):
        # 'self' explanatory
        if self.game.game_over:
            return
        if self.game.initial_phase:
            self.initial_placement()
            return

        self.buy_actions()

        while self.game.actions[self.get_current_color()] > 0:
            if self.game.game_over:
                return 
            if self.fire_turret_check():
                continue
            if self.upgrade_pawn_to_turret():
                continue
            if not self.decide_move():
                self.end_game_with_draw()
                break

        current_color = self.get_current_color()
        if current_color == "black":
            self.turn_count += 1
        self.end_turn_with_farm_count(current_color)
        self.game.advance_turn()
        self.cumulative_reward = 0

    def buy_actions(self):
        '''buys all actions possible'''
        color = self.get_current_color()
        while self.game.action_points[color] >= 3:
            self.game.action_points[color] -= 3
            self.game.actions[color] += 1

    def get_current_color(self):
        return "white" if self.game.turn.lower().startswith("white") else "black"

    def initial_placement(self):
        if self.game.game_over:
            return 
        color = self.get_current_color()
        if self.game.turn.endswith("king"):
            self.place_king(color)
        elif self.game.turn.endswith("farm"):
            self.place_farm(color)

    def place_king(self, color):
        #ai player randomly places king
        if self.game.game_over:
            return
        placed = False
        while not placed:
            row, col = random.randint(0, 7), random.randint(0, 7)
            if self.game.board.is_valid_initial_placement(row, col) and self.game.board.place_piece(row, col, PieceType.KING, color):
                placed = True
                self.place_farm_next_to_king(row, col, color)
                self.game.advance_turn()

    def place_farm_next_to_king(self, king_row, king_col, color):
        if self.game.game_over:
            return
        adjacent_positions = [(king_row - 1, king_col), (king_row + 1, king_col), (king_row, king_col - 1), (king_row, king_col + 1)]
        random.shuffle(adjacent_positions)

        for row, col in adjacent_positions:
            if self.game.board.is_valid_position(row, col) and self.game.board.get_piece_at(row, col) is None:
                self.game.board.place_piece(row, col, PieceType.FARM, color)
                break  # NEED THIS TO ONLY PLACE 1 FARM
        self.game.advance_turn()

    def place_farm(self, color):
        '''not sure if I even need this but dont want to break things'''
        if self.game.game_over:
            return
        king_pos = self.game.board.king_positions[color]
        if king_pos:
            self.place_farm_next_to_king(king_pos[0], king_pos[1], color)
        else:
            self.place_king(color)

    def find_valid_moves(self):
        if self.game.game_over:
            return []
        color = self.get_current_color()
        valid_moves = []

        # Find all valid pawn placement positions
        for row in range(8):
            for col in range(8):
                if (self.game.board.is_adjacent_to_piece(row, col, color) and 
                    self.game.board.is_valid_position(row, col) and 
                    self.game.board.get_piece_at(row, col) is None):
                    valid_moves.append(('place_pawn', row, col))

        # Find all pawns
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.PAWN and piece.color == color:
                    valid_moves.append(('upgrade_pawn', row, col, PieceType.FARM))
                    valid_moves.append(('upgrade_pawn', row, col, PieceType.TURRET))
                    valid_moves.append(('upgrade_pawn', row, col, PieceType.SHIELD))

        # Find all potential turret firing moves
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.TURRET and piece.color == color:
                    valid_targets = self.game.find_valid_targets_for_turret(row, col)
                    for target_row, target_col in valid_targets:
                        valid_moves.append(('fire_turret', row, col, target_row, target_col))

        return valid_moves

    def fire_turret_check(self):
        if self.game.game_over:
            return False

        color = self.get_current_color()
        valid_moves = self.find_valid_moves()
        has_valid_turret_moves = False

        for move in valid_moves:
            if move[0] == 'fire_turret':
                has_valid_turret_moves = True
                turret_row, turret_col, target_row, target_col = move[1], move[2], move[3], move[4]
                target_piece = self.game.board.get_piece_at(target_row, target_col)
                if target_piece and target_piece.piece_type == PieceType.KING:
                    self.game.valid_targets = self.game.find_valid_targets_for_turret(turret_row, turret_col)
                    self.game.fire_turret(turret_row, turret_col, target_row, target_col)
                    self.cumulative_reward += 500  
                    self.log_action(move, 'win', exploration=False)
                    self.data_collector.log_game_end(self.episode) 
                    self.game.game_over = True
                    self.game.winner = self.player_name
                    return True 
                else:
                    self.game.valid_targets = self.game.find_valid_targets_for_turret(turret_row, turret_col) #NEED THIS
                    self.game.fire_turret(turret_row, turret_col, target_row, target_col)
                    valid_moves = self.find_valid_moves()
                    return True
        
        return has_valid_turret_moves

    def decide_move(self):
        if self.game.game_over:
            return False
        color = self.get_current_color()
        valid_moves = self.find_valid_moves()
        if valid_moves:
            state = self.get_state()
            move, exploration = self.choose_action(state, valid_moves)

            # Logs the action and board state evaluation
            self.log_action(move, 'in_progress', exploration)
            return True
        return False

    def end_turn_with_farm_count(self, color):
        if self.game.game_over:
            return

        farm_count = self.game.board.count_farms(color)
        self.game.action_points[color] += farm_count

    def end_game_with_draw(self):
        winner = None
        self.log_action(None, 'draw', exploration=False)
        self.data_collector.log_game_end(self.episode) # Log the end of the game
        self.game.game_over = True
        self.game.winner = winner

        # Decay epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        print(f"End of episode {self.episode}: epsilon={self.epsilon:.4f}")

    def get_diagonal_positions(self, row, col):
        diagonals = []
        for num in range(1, 8):
            diagonals.extend([(row - num, col - num), (row - num, col + num),(row + num, col - num), (row + num, col + num)])
        return diagonals

    def upgrade_pawn_to_turret(self):
        color = self.get_current_color()
        enemy_king_color = "black" if color == "white" else "white"
        enemy_king_pos = self.game.board.king_positions[enemy_king_color]

        if not enemy_king_pos:
            return False

        enemy_king_row, enemy_king_col = enemy_king_pos
        diagonal_positions = self.get_diagonal_positions(enemy_king_row, enemy_king_col)

        for row, col in diagonal_positions:
            if self.game.board.is_valid_position(row, col):
                piece = self.game.board.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.PAWN and piece.color == color:
                    self.perform_action(('upgrade_pawn', row, col, PieceType.TURRET))
                    
                    return True
                else:
                    pass
        return False