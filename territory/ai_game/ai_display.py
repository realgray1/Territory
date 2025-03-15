import pygame
import sys
from game.logic import Game
from game.board import Board
from game.display import draw_board, draw_pieces, draw_right_panel, handle_mouse_button_down

pygame.init()
BOARD_SIZE = 8
SQUARE_SIZE = 80
RIGHT_PANEL_WIDTH = 200
WIDTH, HEIGHT = SQUARE_SIZE * BOARD_SIZE, SQUARE_SIZE * BOARD_SIZE
screen = pygame.display.set_mode((WIDTH + RIGHT_PANEL_WIDTH, HEIGHT))
#pygame.display.set_caption('Territory - Play vs AI')  # Remove this line

game = Game()

def start_game_display():
    pygame.display.set_caption('Territory - Play vs AI')  # Set caption for AI mode
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_board()
        buttons = draw_right_panel()
        draw_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_button_down(event, buttons)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    start_game_display()