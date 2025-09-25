from ai_game.ai_pieces import PieceType

def evaluate_board(game):
    score = 0
    for row in range(8):
        for col in range(8):
            piece = game.board.get_piece_at(row, col)
            if piece:
                piece_value = get_piece_value(piece)
                score += piece_value

    return score

def get_piece_value(piece):
    piece_values = {
        PieceType.KING: 1000,
        PieceType.PAWN: 3,
        PieceType.FARM: 7,
        PieceType.TURRET: 6,
        PieceType.SHIELD: 6
    }
    value = piece_values.get(piece.piece_type, 0)
    return value if piece.color == "white" else -value