import pygame
from game.logic import Game
from game.board import Board
from game.display2 import draw_board, draw_right_panel, draw_pieces, handle_mouse_button_down

pygame.init()
BOARD_SIZE = 8
SQUARE_SIZE = 80
RIGHT_PANEL_WIDTH = 200
WIDTH, HEIGHT = SQUARE_SIZE * BOARD_SIZE, SQUARE_SIZE * BOARD_SIZE
screen = pygame.display.set_mode((WIDTH + RIGHT_PANEL_WIDTH, HEIGHT))

# Colors
BACKGROUND_COLOR = (220, 220, 220)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHESS_GREEN = (118, 150, 86)
SELECTED_COLOR = (0, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
REALGRAY = (96, 96, 96, 128)  # thats me!
HOVER_COLOR = (150, 150, 150, 100) 

# Pieces
assets = "assets/"
piece_images = {
    "white_king": pygame.image.load(assets + "white_king.png"),
    "black_king": pygame.image.load(assets + "black_king.png"),
    "white_farm": pygame.image.load(assets + "white_farm.png"),
    "black_farm": pygame.image.load(assets + "black_farm.png"),
    "white_pawn": pygame.image.load(assets + "white_pawn.png"),
    "black_pawn": pygame.image.load(assets + "black_pawn.png"),
    "white_turret": pygame.image.load(assets + "white_turret.png"),
    "black_turret": pygame.image.load(assets + "black_turret.png"),
    "white_shield": pygame.image.load(assets + "white_shield.png"),
    "black_shield": pygame.image.load(assets + "black_shield.png"),
}

game = Game()   #Game is game

DOT_COLOR = (169, 169, 169)  # My dots

def start_game_display():
    pygame.display.set_caption('Territory - Play Side by Side')
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_board(screen, game, BOARD_SIZE, SQUARE_SIZE, WHITE, CHESS_GREEN, REALGRAY, DOT_COLOR)
        buttons = draw_right_panel(screen, game, WIDTH, HEIGHT, RIGHT_PANEL_WIDTH, 
                                   BACKGROUND_COLOR, BLACK, WHITE, RED, GOLD, HOVER_COLOR, piece_images)
        draw_pieces(screen, game, BOARD_SIZE, SQUARE_SIZE, piece_images)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_button_down(event, buttons, game, SQUARE_SIZE)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    start_game_display()