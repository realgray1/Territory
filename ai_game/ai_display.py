import pygame
import sys
from ai_game.ai_logic import Game
from ai_game.q_learning_ai import QLearningAI
from ai_game.ai_pieces import PieceType

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
BLUE = (0, 0, 255)
SELECTED_COLOR = (0, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

def reset_game():
    global game, q_learning_ai
    game = Game()
    q_learning_ai = QLearningAI(game, player_name="AI Player")
    q_learning_ai.load_q_table('qtable/q_table.pkl')

game = Game() #game is game

# Initialize q learning
q_learning_ai = QLearningAI(game, player_name="AI Player")
q_learning_ai.load_q_table('qtable/q_table.pkl')

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            color = WHITE if (row + col) % 2 == 0 else CHESS_GREEN
            pygame.draw.rect(screen, color, rect)

def draw_right_panel():
    pygame.draw.rect(screen, BACKGROUND_COLOR, pygame.Rect(WIDTH, 0, RIGHT_PANEL_WIDTH, HEIGHT))
    font = pygame.font.SysFont('Arial', 24)

    if game.game_over:
        winner_text = font.render(f"{game.winner} wins!", True, RED)
        screen.blit(winner_text, (WIDTH + 20, 30))

        thanks_text = font.render("Q table saved.", True, BLACK)
        screen.blit(thanks_text, (WIDTH + 20, 60))

        play_again_button = pygame.Rect(WIDTH + 20, 100, 160, 40)
        pygame.draw.rect(screen, BLUE, play_again_button)
        play_again_text = font.render("Play Again", True, BLACK)
        screen.blit(play_again_text, (WIDTH + 55, 110))

        return [play_again_button]

    turn_text = font.render(f"Turn: {game.turn.replace('_', ' ').capitalize()}", True, BLACK)
    screen.blit(turn_text, (WIDTH + 20, 30))

    current_color = "white" if game.turn.lower().startswith("white") else "black"
    current_actions_text = font.render(f"{current_color.capitalize()} Actions: {game.actions[current_color]}", True, BLACK)
    screen.blit(current_actions_text, (WIDTH + 20, 80))

    white_action_points_text = font.render(f"White AP: {game.action_points['white']}", True, BLACK)
    screen.blit(white_action_points_text, (WIDTH + 20, 140))
    black_action_points_text = font.render(f"Black AP: {game.action_points['black']}", True, BLACK)
    screen.blit(black_action_points_text, (WIDTH + 20, 170))

    buttons = []

    if not game.initial_phase:
        place_pawn_button = pygame.Rect(WIDTH + 20, 230, 160, 40)
        button_color = (0, 255, 0)
        pygame.draw.rect(screen, button_color, place_pawn_button)
        pawn_button_text = font.render("Place Pawn", True, BLACK)
        screen.blit(pawn_button_text, (WIDTH + 40, 240))
        buttons.append(place_pawn_button)

        farm_button = pygame.Rect(WIDTH + 20, 280, 50, 50)
        turret_button = pygame.Rect(WIDTH + 75, 280, 50, 50)
        shield_button = pygame.Rect(WIDTH + 130, 280, 50, 50)

        pygame.draw.rect(screen, WHITE, farm_button)
        pygame.draw.rect(screen, WHITE, turret_button)
        pygame.draw.rect(screen, WHITE, shield_button)

        screen.blit(pygame.transform.scale(piece_images["white_farm"], (50, 50)), (WIDTH + 20, 280))
        screen.blit(pygame.transform.scale(piece_images["white_turret"], (50, 50)), (WIDTH + 75, 280))
        screen.blit(pygame.transform.scale(piece_images["white_shield"], (50, 50)), (WIDTH + 130, 280))

        buttons.extend([farm_button, turret_button, shield_button])

        fire_turret_button = pygame.Rect(WIDTH + 20, 340, 160, 40)
        pygame.draw.rect(screen, RED, fire_turret_button)
        fire_turret_text = font.render("Fire Turret", True, BLACK)
        screen.blit(fire_turret_text, (WIDTH + 40, 350))
        buttons.append(fire_turret_button)

        buy_action_button = pygame.Rect(WIDTH + 20, 390, 160, 40)
        pygame.draw.rect(screen, GOLD, buy_action_button)
        buy_action_text = font.render("Buy Action", True, BLACK)
        screen.blit(buy_action_text, (WIDTH + 40, 400))
        buttons.append(buy_action_button)

        cancel_button = pygame.Rect(WIDTH + 20, 440, 160, 40)
        pygame.draw.rect(screen, (155, 161, 157), cancel_button)
        cancel_text = font.render("Cancel", True, BLACK)
        screen.blit(cancel_text, (WIDTH + 40, 450))
        buttons.append(cancel_button)

        pass_turn_button = pygame.Rect(WIDTH + 20, 490, 160, 40)
        pygame.draw.rect(screen, (128, 128, 128), pass_turn_button)
        pass_turn_text = font.render("Pass Turn", True, BLACK)
        screen.blit(pass_turn_text, (WIDTH + 40, 500))
        buttons.append(pass_turn_button)

    return buttons

def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(8):
            piece = game.board.get_piece_at(row, col)
            if piece:
                piece_image_key = f"{piece.color}_{piece.piece_type.value}"
                piece_image = piece_images.get(piece_image_key)
                if piece_image:
                    piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def handle_mouse_button_down(event, buttons):
    for button in buttons:
        if button.collidepoint(event.pos):
            if game.game_over:
                q_learning_ai.save_q_table('qtable/q_table.pkl')
                if button == buttons[0]:  # Play Again
                    reset_game()
                return

            if button == buttons[0]:  # Place Pawn
                if not game.upgrade_mode and not game.firing_mode:
                    game.initiate_pawn_placement()
            elif button == buttons[1]:  # Farm
                if not game.firing_mode and not game.pawn_placement_mode:
                    game.initiate_pawn_upgrade("farm")
            elif button == buttons[2]:  # Turret
                if not game.firing_mode and not game.pawn_placement_mode:
                    game.initiate_pawn_upgrade("turret")
            elif button == buttons[3]:  # Shield
                if not game.firing_mode and not game.pawn_placement_mode:
                    game.initiate_pawn_upgrade("shield")
            elif button == buttons[4]:  # Fire Turret
                if not game.upgrade_mode and not game.pawn_placement_mode:
                    game.initiate_turret_firing()
            elif button == buttons[5]:  # Buy Action
                if not game.upgrade_mode and not game.firing_mode and not game.pawn_placement_mode:
                    game.buy_action()
            elif button == buttons[6]:  # Cancel
                game.cancel_action()
            elif button == buttons[7]:  # Pass Turn
                if not game.upgrade_mode and not game.firing_mode and not game.pawn_placement_mode:
                    game.pass_turn()
            return

    row, col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
    if game.firing_mode:
        if game.selected_turret:
            if game.validate_turret_target(row, col):
                turret_row, turret_col = game.selected_turret
                game.fire_turret(turret_row, turret_col, row, col)
            else:
                print("Invalid target for turret firing.")
        else:
            game.select_turret_to_fire(row, col)
    else:
        game.handle_click(row, col)

def start_ai_game_display():
    pygame.display.set_caption('Territory - Play vs AI')
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_board()
        buttons = draw_right_panel()
        draw_pieces()

        if game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    q_learning_ai.save_q_table('qtable/q_table.pkl')  # Save Q-table
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_mouse_button_down(event, buttons)
        else:
            if game.turn.startswith("white"):  # Human player's turn
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        q_learning_ai.save_q_table('qtable/q_table.pkl')
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        handle_mouse_button_down(event, buttons)
            else:  # AI player's turn
                if game.initial_phase:
                    q_learning_ai.initial_placement()
                else:
                    q_learning_ai.buy_actions()  # Buy me up

                    while game.actions["black"] > 0:
                        if game.game_over:
                            break
                        if q_learning_ai.fire_turret_check():
                            continue
                        if q_learning_ai.upgrade_pawn_to_turret():
                            continue
                        if not q_learning_ai.decide_move():
                            q_learning_ai.end_game_with_draw()  # End the game as a draw
                            break

                    game.end_turn() 

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    start_ai_game_display()