from ai_game.ai_pieces import Piece, PieceType

class Board:
    def __init__(self):
        self.board = [[None for num in range(8)] for num in range(8)]
        self.king_positions = {"white": None, "black": None}

    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        else:
            return None

    def place_piece(self, row, col, piece_type, color):
        if self.is_valid_position(row, col) and self.board[row][col] is None:
            newpiece = Piece(color, piece_type)
            self.board[row][col] = newpiece
            newpiece.position = (row, col)
            if piece_type == PieceType.KING:
                self.king_positions[color] = (row, col)
            return True
        return False

    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_valid_initial_placement(self, row, col):
        # King can't be placed in the center 4 squares
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        return (row, col) not in center_squares

    def is_adjacent_to_king(self, row, col, color):
        king_pos = self.king_positions[color]
        king_row, king_col = king_pos
        adjacent_positions = [(king_row-1, king_col), (king_row+1, king_col), (king_row, king_col-1), (king_row, king_col+1)]
        return (row, col) in adjacent_positions

    def is_adjacent_to_piece(self, row, col, color):
        adjacent_positions = [
            (row-1, col), (row+1, col), (row, col-1), (row, col+1)
        ]
        for adj_row, adj_col in adjacent_positions:
            if self.is_valid_position(adj_row, adj_col):
                piece = self.get_piece_at(adj_row, adj_col)
                if piece and piece.color == color:
                    return True
        return False

    def has_pawn(self, color):
        """Checks if the player has a pawn."""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.PAWN and piece.color == color:
                    return True
        return False

    def has_turret(self, color):
        """Checks if the player has a turret."""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.TURRET and piece.color == color:
                    return True
        return False

    def count_farms(self, color):
        """Counts the number of farms a player has"""
        farm_count = 0
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.FARM and piece.color == color:
                    farm_count += 1
        return farm_count

    def find_king(self, color):
        """Stores the king's position for future reference"""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.piece_type == PieceType.KING and piece.color == color:
                    return row, col
        return None