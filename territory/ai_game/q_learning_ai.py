import random
import numpy as np
from ai_game.ai_pieces import PieceType, Piece
from ai_game.ai_logic import Game
from ai_game.data_collection import DataCollector
from ai_game.board_evaluation import evaluate_board

class QLearningAI(Game):
    def __init__(self, game, player_name, alpha=0.1, gamma=0.9, epsilon=0.1, epsilon_decay=0.995, min_epsilon=0.01, episode=1):
        super().__init__()
        self.game = game
        self.data_collector = DataCollector()
        self.player_name = player_name
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon
        self.min_epsilon = min_epsilon  # Minimum value for epsilon
        self.q_table = {}  # Initialize Q-table as an empty dictionary
        self.episode = episode  # Current training episode
        self.turn_count = 0  # Track the number of turns in the current episode
        self.previous_board_evaluation = evaluate_board(self.game)  # Initial board evaluation

    def get_state(self):
        # Convert the current game state to a tuple (hashable type)
        return tuple([tuple(row) for row in self.game.board.board])

    def choose_action(self, state, valid_moves):
        exploration = False
        if not valid_moves:
            return None, exploration
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

    def update_q_value(self, state, action, reward, next_state, next_valid_moves):
        current_q = self.q_table.get((state, action), 0)
        if next_valid_moves:
            next_q = max([self.q_table.get((next_state, next_action), 0) for next_action in next_valid_moves])
        else:
            next_q = 0
        
        new_q = current_q + self.alpha * (reward + self.gamma * next_q - current_q)
        q_value_change = abs(new_q - current_q)
        self.q_table[(state, action)] = new_q
        return q_value_change

    def calculate_reward(self, previous_evaluation, current_evaluation, action):
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
            # Perform the action
            self.perform_action(action)
        
        current_board_evaluation = evaluate_board(self.game)
        reward = self.calculate_reward(previous_board_evaluation, current_board_evaluation, action)
        q_value_change = self.update_q_value(state, action, reward, self.get_state(), self.find_valid_moves())
        
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
            self.q_table.get((state, action), 0) if action else None, q_value_change, exploration, self.game.turn
        )

    def perform_action(self, action):
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
            self.game.actions[color] -= 1

    def make_move(self):
        if self.game.game_over:
            return  # Do not make any moves if the game is over

        self.buy_actions()  # Buy actions at the start of the turn
        if self.game.initial_phase:
            self.initial_placement()
        else:
            actions_remaining = True
            while actions_remaining:
                if self.game.game_over:
                    return  # Do not make any moves if the game is over
                if self.game.actions[self.get_current_color()] > 0:
                    if self.fire_turret_at_king_if_possible():
                        continue  # Continue to the next action after firing a turret at non-king targets
                    if not self.decide_move():
                        self.end_game_with_draw()  # End the game with a draw if no valid moves are left
                        actions_remaining = False
                else:
                    actions_remaining = False
        current_color = self.get_current_color()
        self.end_turn_with_farm_count(current_color)
        self.game.advance_turn()  # Pass the turn back to the other AI player

    def buy_actions(self):
        color = self.get_current_color()
        while self.game.action_points[color] >= 3:
            self.game.action_points[color] -= 3  # Deduct 3 action points
            self.game.actions[color] += 1

    def get_current_color(self):
        return "white" if self.game.turn.lower().startswith("white") else "black"

    def initial_placement(self):
        if self.game.game_over:
            return  # Do not place any pieces if the game is over

        color = self.get_current_color()
        if self.game.turn.endswith("king"):
            self.place_king(color)
        elif self.game.turn.endswith("farm"):
            self.place_farm(color)

    def place_king(self, color):
        if self.game.game_over:
            return  # Do not place any pieces if the game is over

        placed = False
        while not placed:
            row, col = random.randint(0, 7), random.randint(0, 7)
            if self.game.board.place_piece(row, col, PieceType.KING, color):
                placed = True
                self.place_farm_next_to_king(row, col, color)  # Place farm next to king immediately
                self.game.advance_turn()  # Advance turn after placing both king and farm

    def place_farm_next_to_king(self, king_row, king_col, color):
        if self.game.game_over:
            return  # Do not place any pieces if the game is over

        adjacent_positions = [
            (king_row - 1, king_col), (king_row + 1, king_col),
            (king_row, king_col - 1), (king_row, king_col + 1)
        ]
        random.shuffle(adjacent_positions)
        for row, col in adjacent_positions:
            if self.game.board.is_valid_position(row, col) and self.game.board.get_piece_at(row, col) is None:
                self.game.board.place_piece(row, col, PieceType.FARM, color)
                return

    def place_farm(self, color):
        if self.game.game_over:
            return  # Do not place any pieces if the game is over

        king_pos = self.game.board.king_positions[color]
        if king_pos:
            self.place_farm_next_to_king(king_pos[0], king_pos[1], color)
        else:
            self.place_king(color)  # Ensure the King is placed first

    def find_valid_moves(self):
        if self.game.game_over:
            return []  # No valid moves if the game is over

        color = self.get_current_color()
        valid_moves = []

        # Find all valid pawn placement positions
        for row in range(8):
            for col in range(8):
                if (self.game.board.is_adjacent_to_piece(row, col, color) and 
                    self.game.board.is_valid_position(row, col) and 
                    self.game.board.get_piece_at(row, col) is None):
                    valid_moves.append(('place_pawn', row, col))

        # Find all pawns that can be upgraded and their upgrade options
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.PAWN and piece.color == color:
                    valid_moves.append(('upgrade_pawn', row, col, PieceType.FARM))
                    valid_moves.append(('upgrade_pawn', row, col, PieceType.TURRET))
                    valid_moves.append(('upgrade_pawn', row, col, PieceType.SHIELD))

        # Find all valid turret firing targets
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.TURRET and piece.color == color:
                    valid_targets = self.game.find_valid_targets_for_turret(row, col)
                    for target_row, target_col in valid_targets:
                        valid_moves.append(('fire_turret', row, col, target_row, target_col))

        return valid_moves

    def fire_turret_at_king_if_possible(self):
        if self.game.game_over:
            return False  # Do not fire turret if the game is over

        color = self.get_current_color()
        valid_moves = self.find_valid_moves()
        for move in valid_moves:
            if move[0] == 'fire_turret':
                target_row, target_col = move[3], move[4]
                target_piece = self.game.board.get_piece_at(target_row, target_col)
                if target_piece and target_piece.piece_type == PieceType.KING:
                    self.game.valid_targets = self.game.find_valid_targets_for_turret(move[1], move[2])
                    self.game.fire_turret(move[1], move[2], target_row, target_col)
                    self.log_action(move, 'win', exploration=False)
                    self.data_collector.log_game_end(self.episode)  # Log the end of the game
                    self.game.game_over = True
                    self.game.winner = self.player_name
                    return True  # End the game if the king is hit
        return False

    def decide_move(self):
        if self.game.game_over:
            return False  # Do not decide move if the game is over

        color = self.get_current_color()
        valid_moves = self.find_valid_moves()
        if valid_moves:
            state = self.get_state()
            move, exploration = self.choose_action(state, valid_moves)
            
            # Log the action and board state evaluation before performing the action
            self.log_action(move, 'in_progress', exploration)
            return True
        return False

    def end_turn_with_farm_count(self, color):
        if self.game.game_over:
            return  # Do not end turn if the game is over

        farm_count = self.game.board.count_farms(color)
        self.game.action_points[color] += farm_count

    def end_game_with_draw(self):
        winner = None
        self.log_action(None, 'draw', exploration=False)
        self.data_collector.log_game_end(self.episode)  # Log the end of the game
        self.game.game_over = True
        self.game.winner = winner
        # Decay epsilon after each episode
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        print(f"End of episode {self.episode}: epsilon={self.epsilon:.4f}")