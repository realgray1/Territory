from enum import Enum

class PieceType(Enum):
    KING = "king"
    FARM = "farm"
    PAWN = "pawn"
    TURRET = "turret"
    SHIELD = "shield"

class Piece:
    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type
        self.position = None