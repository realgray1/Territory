import random
from ai_game.ai_pieces import PieceType, Piece
from ai_game.ai_logic import Game
from ai_game.data_collection import DataCollector

class SimpleAI(Game):
    def __init__(self, game, player_name):
        super().__init__()
        self.game = game
        self.data_collector = DataCollector()
        self.player_name = player_name

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
                        self.end_game_with_loss()  # End the game if no valid moves are left
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
                    self.data_collector.log_data(
                        self.data_collector.serialize_game_state(self.game),
                        self.data_collector.serialize_action('fire_turret', {'from': (move[1], move[2]), 'to': (target_row, target_col)}),
                        'win'  # Assuming hitting the king results in a win
                    )
                    print(f"{self.player_name} fires turret from {(move[1], move[2])} to {(target_row, target_col)}")
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
            move = random.choice(valid_moves)
            if move[0] == 'place_pawn':
                self.game.board.place_piece(move[1], move[2], PieceType.PAWN, color)
                self.data_collector.log_data(
                    self.data_collector.serialize_game_state(self.game),
                    self.data_collector.serialize_action('place_pawn', {'row': move[1], 'col': move[2]}),
                    'in_progress'
                )
                print(f"{self.player_name} places pawn at {(move[1], move[2])}")
                self.game.actions[color] -= 1
            elif move[0] == 'upgrade_pawn':
                self.game.board.board[move[1]][move[2]] = Piece(color, move[3])
                self.data_collector.log_data(
                    self.data_collector.serialize_game_state(self.game),
                    self.data_collector.serialize_action('upgrade_pawn', {'row': move[1], 'col': move[2], 'to': move[3].name}),
                    'in_progress'
                )
                print(f"{self.player_name} upgrades pawn at {(move[1], move[2])} to {move[3].name}")
                self.game.actions[color] -= 1
            elif move[0] == 'fire_turret':
                self.game.valid_targets = self.game.find_valid_targets_for_turret(move[1], move[2])
                self.game.fire_turret(move[1], move[2], move[3], move[4])
                self.data_collector.log_data(
                    self.data_collector.serialize_game_state(self.game),
                    self.data_collector.serialize_action('fire_turret', {'from': (move[1], move[2]), 'to': (move[3], move[4])}),
                    'in_progress'
                )
                print(f"{self.player_name} fires turret from {(move[1], move[2])} to {(move[3], move[4])}")
                self.game.actions[color] -= 1
            return True
        return False

    def end_turn_with_farm_count(self, color):
        if self.game.game_over:
            return  # Do not end turn if the game is over

        farm_count = self.game.board.count_farms(color)
        self.game.action_points[color] += farm_count

    def end_game_with_loss(self):
        winner = "Player 1" if self.player_name == "Player 2" else "Player 2"
        self.data_collector.log_data(
            self.data_collector.serialize_game_state(self.game),
            {'action': 'game_over', 'winner': winner},
            'loss'
        )
        self.game.game_over = True
        self.game.winner = winner
        print(f"{self.player_name} has no valid moves left and loses the game.")