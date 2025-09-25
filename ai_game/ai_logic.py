from ai_game.ai_board import Board
from ai_game.ai_pieces import Piece, PieceType

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "white_king"
        self.initial_phase = True
        self.actions = {"white": 1, "black": 1}
        self.action_points = {"white": 0, "black": 0}
        self.pawn_placement_mode = False
        self.upgrade_mode = False
        self.selected_pawn = None
        self.upgrade_type = None
        self.firing_mode = False
        self.selected_turret = None
        self.valid_targets = []
        self.game_over = False 
        self.winner = None
        self.scores = {"Player 1": 0, "Player 2": 0}
        self.player1_color = "white"
        self.player2_color = "black"

    def reset_game(self):
        scores = self.scores.copy() 
        player1_color = self.player1_color
        player2_color = self.player2_color
        self.__init__()
        self.scores = scores
        self.player1_color = player1_color
        self.player2_color = player2_color

    def handle_click(self, row, col):
        if self.initial_phase:
            self.handle_initial_placement(row, col)
        elif self.pawn_placement_mode:
            self.place_pawn(row, col)
        elif self.upgrade_mode:
            self.select_pawn(row, col)
        else:
            pass

    def handle_initial_placement(self, row, col):
        color = "white" if self.turn.startswith("white") else "black"
        piece_type = PieceType.KING if self.turn.endswith("king") else PieceType.FARM
        if self.board.is_valid_initial_placement(row, col):
            if piece_type == PieceType.KING or self.board.is_adjacent_to_king(row, col, color):
                if self.board.place_piece(row, col, piece_type, color):
                    print(f"{color.capitalize()} {piece_type} placed at ({row}, {col})")
                    self.advance_turn()
        else:
            print(f"{piece_type.name.capitalize()} cannot be placed in the center")

    def advance_turn(self):
        if self.turn == "white_king":
            self.turn = "white_farm"
        elif self.turn == "white_farm":
            self.turn = "black_king"
        elif self.turn == "black_king":
            self.turn = "black_farm"
        elif self.turn == "black_farm":
            self.initial_phase = False
            self.turn = "white"
            self.action_points["white"] = 0
            self.action_points["black"] = 1  # Black player starts with 1 action point
        elif self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"
        self.reset_actions()

    def reset_actions(self):
        current_color = "white" if self.turn.lower() == "white" else "black"
        self.actions[current_color] = 1

    def initiate_pawn_placement(self):
        """sets the game to pawn placing mode."""
        current_color = "white" if self.turn.lower() == "white" else "black"
        if self.actions[current_color] > 0:
            self.pawn_placement_mode = True
            print(f"{current_color.capitalize()} can now place a pawn.")

    def place_pawn(self, row, col):
        """checks for valid pawn placement"""
        current_color = "white" if self.turn.lower() == "white" else "black"
        if self.board.is_adjacent_to_piece(row, col, current_color) and self.board.is_valid_position(row, col):
            if self.board.place_piece(row, col, PieceType.PAWN, current_color):
                self.actions[current_color] -= 1
                self.pawn_placement_mode = False
                print(f"{current_color.capitalize()} Pawn placed at ({row, col}).")
        else:
            print("Invalid pawn placement. Must be connected to your island.")

    def initiate_pawn_upgrade(self, upgrade_type):
        """upgrade mode"""
        current_color = "white" if self.turn.lower() == "white" else "black"
        if self.actions[current_color] > 0 and self.board.has_pawn(current_color):
            self.upgrade_mode = True
            self.upgrade_type = PieceType[upgrade_type.upper()]
            print(f"{current_color.capitalize()} can now select a pawn to upgrade to {upgrade_type}.")
        else:
            print(f"{current_color.capitalize()} has no pawns to upgrade or no actions remaining.")

    def select_pawn(self, row, col):
        """Player chooses which pawn to upgrade"""
        current_color = "white" if self.turn.lower() == "white" else "black"
        piece = self.board.get_piece_at(row, col)
        if piece and piece.piece_type == PieceType.PAWN and piece.color == current_color:
            self.selected_pawn = (row, col)
            self.upgrade_pawn(self.upgrade_type)

    def upgrade_pawn(self, new_type):
        if not self.selected_pawn:
            return
        row, col = self.selected_pawn
        current_color = "white" if self.turn.lower() == "white" else "black"
        if isinstance(new_type, PieceType):
            self.board.board[row][col] = Piece(current_color, new_type)
            self.actions[current_color] -= 1
            self.upgrade_mode = False
            self.selected_pawn = None
            self.upgrade_type = None
            print(f"{current_color.capitalize()} Pawn at ({row, col}) upgraded to {new_type}.")
        else:
            print(f"Invalid piece type: {new_type}")

    def cancel_upgrade(self):
        """Cancels the pawn upgrade mode"""
        self.upgrade_mode = False
        self.selected_pawn = None
        self.upgrade_type = None
        print("Pawn upgrade canceled.")

    def initiate_turret_firing(self):
        """Initiate the turret firing mode"""
        current_color = "white" if self.turn.lower() == "white" else "black"
        if self.actions[current_color] > 0 and self.board.has_turret(current_color):
            self.firing_mode = True
            print(f"{current_color.capitalize()} can now select a turret to fire.")
        else:
            print(f"{current_color.capitalize()} has no turrets to fire or no actions remaining.")

    def select_turret_to_fire(self, row, col):
        current_color = "white" if self.turn.lower() == "white" else "black"
        piece = self.board.get_piece_at(row, col)
        if piece and piece.piece_type == PieceType.TURRET and piece.color == current_color:
            valid_targets = self.find_valid_targets_for_turret(row, col)
            if valid_targets:
                self.selected_turret = (row, col)
                self.valid_targets = valid_targets
                print(f"{current_color.capitalize()} Turret at ({row, col}) selected, Choose a diagonal target.")
            else:
                print(f"No valid targets for turret at ({row, col}).")

    def find_valid_targets_for_turret(self, turret_row, turret_col):
        valid_targets = []
        current_color = "white" if self.turn.lower().startswith("white") else "black"
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 4 diagonal directions

        for row_step, col_step in directions:
            row, col = turret_row + row_step, turret_col + col_step
            while 0 <= row < 8 and 0 <= col < 8:
                piece = self.board.get_piece_at(row, col)
                if piece:
                    if piece.color != current_color:
                        valid_targets.append((row, col))
                    break
                row += row_step
                col += col_step

        return valid_targets

    def validate_turret_target(self, target_row, target_col):
        return (target_row, target_col) in self.valid_targets

    def fire_turret(self, turret_row, turret_col, target_row, target_col):
        """Fire the turret"""
        if self.validate_turret_target(target_row, target_col):
            target_piece = self.board.get_piece_at(target_row, target_col)
            if target_piece:
                if not hasattr(self.board, 'history'):
                    self.board.history = []
                self.board.history.append((target_piece, (target_row, target_col)))  # Save the removed piece and its location for undo

                if target_piece.piece_type == PieceType.SHIELD:  # Converts shields into pawns
                    self.board.board[target_row][target_col] = Piece(target_piece.color, PieceType.PAWN)
                    print(f"Turret at ({turret_row, turret_col}) hit a shield at ({target_row, target_col}).")
                elif target_piece.piece_type == PieceType.KING:  # If it hits the king, game over
                    self.board.board[target_row][target_col] = None
                    self.game_over = True
                    self.winner = "Player 2" if target_piece.color == self.player1_color else "Player 1"
                    self.scores[self.winner] += 1 
                    print(f"Game over! {self.winner} wins!")
                else:
                    self.board.board[target_row][target_col] = None  # Removes the piece
                    print(f"Turret at ({turret_row, turret_col}) fired and removed {target_piece.color} {target_piece.piece_type} at ({target_row, target_col}).")

                self.selected_turret = None
                self.valid_targets = []
                self.firing_mode = False
                self.remove_isolated_pieces(target_piece.color)
                current_color = "white" if self.turn.lower() == "white" else "black"
                self.actions[current_color] -= 1
            else:
                print("No piece at target location.")
        else:
            pass

    def get_connected_pieces(self, start_row, start_col):
        """Uses BFS to find all connected pieces to the king"""
        visited = set()
        mylist = [(start_row, start_col)]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Only horizontal and vertical directions count, no diagonals

        while mylist:
            row, col = mylist.pop(0)
            if (row, col) in visited:
                continue
            visited.add((row, col))
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = self.board.get_piece_at(new_row, new_col)
                    if piece and piece.color == self.board.get_piece_at(start_row, start_col).color:
                        mylist.append((new_row, new_col))
        return visited

    def remove_isolated_pieces(self, color):
        """Removes all pieces that aren't part of the main island"""
        if not self.game_over:
            king_position = self.board.find_king(color)
            connected_pieces = self.get_connected_pieces(*king_position)
            piececount = 0
            removed_pieces = []
            for row in range(8):
                for col in range(8):
                    piece = self.board.get_piece_at(row, col)
                    if piece and piece.color == color and (row, col) not in connected_pieces:
                        removed_pieces.append((piece, (row, col)))
                        self.board.board[row][col] = None
                        piececount += 1
            if piececount > 0:
                self.board.history.append(('isolated', removed_pieces))  # Save the isolated pieces for undo
                if piececount == 1:
                    print('1 isolated piece lost :(')
                elif piececount > 1:
                    print(f"{piececount} isolated pieces lost!")

    def buy_action(self):
        """Allow the player to buy an action if they have at least 3 action points."""
        current_color = "white" if self.turn.lower().startswith("white") else "black"
        if self.action_points[current_color] >= 3:
            self.action_points[current_color] -= 3
            self.actions[current_color] += 1
            print(f"{current_color.capitalize()} bought an action!")
        else:
            print(f"{current_color.capitalize()} does not have the funds.")

    def cancel_action(self):
        """Resets everything. Fixes softlock problems xD"""
        self.pawn_placement_mode = False
        self.upgrade_mode = False
        self.firing_mode = False
        self.selected_pawn = None
        self.upgrade_type = None
        self.selected_turret = None
        self.valid_targets = []
        print("Action cancelled.")

    def pass_turn(self):
        self.end_turn()

    def end_turn(self):
        if self.game_over:
            return
        current_color = "white" if self.turn.lower() == "white" else "black"
        farm_count = self.board.count_farms(current_color)
        self.action_points[current_color] += farm_count  # FARMING

        self.turn = "black" if current_color == "white" else "white"
        self.reset_actions()

    def swap_colors(self):
        self.player1_color, self.player2_color = self.player2_color, self.player1_color
        print(f"Colors swapped. Player 1 is now {self.player1_color.capitalize()} and Player 2 is now {self.player2_color.capitalize()}.")