
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
REALGRAY = (96, 96, 96, 128)  # thats me!
HOVER_COLOR = (150, 150, 150, 100) 
DOT_COLOR = (169, 169, 169)  # My dots

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
            
            # Gray out the middle 4 squares
            if game.initial_phase and 3 <= row <= 4 and 3 <= col <= 4:
                overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                overlay.set_alpha(128)  # Set transparency
                overlay.fill(REALGRAY)
                screen.blit(overlay, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Draw a gray dot to show valid moves
    if game.turn.lower() == "white_farm" or game.turn.lower() == "black_farm":
        what_color = "white" if game.turn.lower() == "white_farm" else "black"
        king_position = game.board.king_positions[what_color]
        if king_position:
            king_row, king_col = king_position
            adjacent_positions = [
                (king_row-1, king_col), (king_row+1, king_col),
                (king_row, king_col-1), (king_row, king_col+1)
            ]
            center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
            for adj_row, adj_col in adjacent_positions:
                if (adj_row, adj_col) not in center_squares and 0 <= adj_row < BOARD_SIZE and 0 <= adj_col < BOARD_SIZE:
                    dot_rect = pygame.Rect(
                        adj_col * SQUARE_SIZE + SQUARE_SIZE // 2 - 5,
                        adj_row * SQUARE_SIZE + SQUARE_SIZE // 2 - 5,
                        10, 10
                    )
                    pygame.draw.ellipse(screen, DOT_COLOR, dot_rect)
    
    # realgray dots
    if game.pawn_placement_mode:
        current_color = "white" if game.turn.lower().startswith("white") else "black"
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Check if this is a valid pawn placement location
                if (game.board.is_adjacent_to_piece(row, col, current_color) and 
                    game.board.is_valid_position(row, col)):
                    dot_rect = pygame.Rect(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2 - 5,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2 - 5,
                        10, 10
                    )
                    pygame.draw.ellipse(screen, DOT_COLOR, dot_rect)
    
    # Highlighhts the pawns
    if game.upgrade_mode:
        current_color = "white" if game.turn.lower().startswith("white") else "black"
        highlight_color = (255, 255, 0)  # Yellow highlight
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = game.board.get_piece_at(row, col)
                if piece and piece.color == current_color and piece.piece_type == PieceType.PAWN:
                    # Draw a highlight border around the pawn
                    border_rect = pygame.Rect(
                        col * SQUARE_SIZE, 
                        row * SQUARE_SIZE, 
                        SQUARE_SIZE, 
                        SQUARE_SIZE
                    )
                    pygame.draw.rect(screen, highlight_color, border_rect, 3)  # 3 pixels wide border
    
    # Highlights turrets
    if game.firing_mode:
        current_color = "white" if game.turn.lower().startswith("white") else "black"
        highlight_color = (255, 0, 0)  # Red highlight for turrets
        target_highlight_color = (0, 255, 0)  # Green highlight for valid targets
        
        if game.selected_turret:
            selected_row, selected_col = game.selected_turret
            
     
            selected_rect = pygame.Rect(
                selected_col * SQUARE_SIZE, 
                selected_row * SQUARE_SIZE, 
                SQUARE_SIZE, 
                SQUARE_SIZE
            )
            pygame.draw.rect(screen, highlight_color, selected_rect, 3)
            
            has_valid_targets = False
            for row, col in game.valid_targets:
                has_valid_targets = True
                target_rect = pygame.Rect(
                    col * SQUARE_SIZE, 
                    row * SQUARE_SIZE, 
                    SQUARE_SIZE, 
                    SQUARE_SIZE
                )
                pygame.draw.rect(screen, target_highlight_color, target_rect, 3)
            
    
            if not has_valid_targets:

                pass
        else:
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    piece = game.board.get_piece_at(row, col)
                    if piece and piece.color == current_color and piece.piece_type == PieceType.TURRET:
                        # Check if this turret has at least one valid target
                        valid_targets = game.find_valid_targets_for_turret(row, col)
                        if valid_targets:
                            border_rect = pygame.Rect(
                                col * SQUARE_SIZE, 
                                row * SQUARE_SIZE, 
                                SQUARE_SIZE, 
                                SQUARE_SIZE
                            )
                            pygame.draw.rect(screen, highlight_color, border_rect, 3)


def draw_right_panel():
    pygame.draw.rect(screen, BACKGROUND_COLOR, pygame.Rect(WIDTH, 0, RIGHT_PANEL_WIDTH, HEIGHT))
    font = pygame.font.SysFont('Arial', 24)
    mouse_pos = pygame.mouse.get_pos() #we NEED this
    current_color = "white" if game.turn.lower().startswith("white") else "black"
    has_actions = game.actions[current_color] > 0

    if game.game_over:
        winner_text = font.render(f"{game.winner} wins!", True, RED)
        screen.blit(winner_text, (WIDTH + 20, 30))

        thanks_text = font.render("Q table saved.", True, BLACK)
        screen.blit(thanks_text, (WIDTH + 20, 60))

        play_again_button = pygame.Rect(WIDTH + 20, 100, 160, 40)
        pygame.draw.rect(screen, BLUE, play_again_button)
        play_again_text = font.render("Play Again", True, BLACK)
        screen.blit(play_again_text, (WIDTH + 55, 110))



        if play_again_button.collidepoint(mouse_pos):
            hover_surface = pygame.Surface((160, 40))
            hover_surface.set_alpha(100)
            hover_surface.fill(HOVER_COLOR)
            screen.blit(hover_surface, (WIDTH + 20, 100, 160, 40))

        return [play_again_button]

    turn_text = font.render(f"Turn: {game.turn.replace('_', ' ').capitalize()}", True, BLACK)
    screen.blit(turn_text, (WIDTH + 20, 30))

    # Actions
    current_color = "white" if game.turn.lower().startswith("white") else "black"
    current_actions_text = font.render(f"Actions: {game.actions[current_color]}", True, BLACK)
    screen.blit(current_actions_text, (WIDTH + 20, 80))

    # helpful texts
    instruction_font = pygame.font.SysFont('Arial', 24)
    instruction_text = ""
    if game.pawn_placement_mode:
        instruction_text = "Place a pawn"
    elif game.upgrade_mode:
        instruction_text = "Select a pawn"
    elif game.firing_mode:
        if game.selected_turret:
            instruction_text = "Select target"
        else:
            instruction_text = "Select turret"

    if instruction_text:
        instruction_render = instruction_font.render(instruction_text, True, (255, 0, 0))
        screen.blit(instruction_render, (WIDTH + 20, 110))

    # APs
    white_action_points_text = font.render(f"White AP: {game.action_points['white']}", True, BLACK)
    screen.blit(white_action_points_text, (WIDTH + 20, 140))
    black_action_points_text = font.render(f"Black AP: {game.action_points['black']}", True, BLACK)
    screen.blit(black_action_points_text, (WIDTH + 20, 170))


    buttons = []

    if not game.initial_phase:
        # Place pawn
        place_pawn_button = pygame.Rect(WIDTH + 20, 300, 160, 40)
        
        if has_actions and not game.upgrade_mode and not game.firing_mode:
            button_color = (0, 255, 0)  
        else:
            button_color = (200, 200, 200) 
        pygame.draw.rect(screen, button_color, place_pawn_button)

        if place_pawn_button.collidepoint(mouse_pos) and has_actions and not game.upgrade_mode and not game.firing_mode:
            hover_surface = pygame.Surface((160, 40))
            hover_surface.set_alpha(100)
            hover_surface.fill(HOVER_COLOR)
            screen.blit(hover_surface, (WIDTH + 20, 300))

        if game.pawn_placement_mode:
            pygame.draw.rect(screen, (255, 0, 0), place_pawn_button, 3)
            
        pawn_button_text = font.render("Place Pawn", True, BLACK if has_actions and not game.upgrade_mode and not game.firing_mode else (120, 120, 120))
        screen.blit(pawn_button_text, (WIDTH + 40, 310))
        buttons.append(place_pawn_button)

        # Upgrade buttons
        piece_color = "white" if game.turn.lower().startswith("white") else "black"
        farm_button = pygame.Rect(WIDTH + 20, 350, 50, 50)
        turret_button = pygame.Rect(WIDTH + 75, 350, 50, 50)
        shield_button = pygame.Rect(WIDTH + 130, 350, 50, 50)

       
        has_pawns = game.board.has_pawn(piece_color)
        can_upgrade = has_actions and has_pawns and not game.pawn_placement_mode and not game.firing_mode

        button_bg_color = WHITE if can_upgrade else (200, 200, 200)
        pygame.draw.rect(screen, button_bg_color, farm_button)
        pygame.draw.rect(screen, button_bg_color, turret_button)
        pygame.draw.rect(screen, button_bg_color, shield_button)

        if game.upgrade_mode:
            if game.upgrade_type == PieceType.FARM:
                pygame.draw.rect(screen, (255, 0, 0), farm_button, 3)  
            elif game.upgrade_type == PieceType.TURRET:
                pygame.draw.rect(screen, (255, 0, 0), turret_button, 3)  
            elif game.upgrade_type == PieceType.SHIELD:
                pygame.draw.rect(screen, (255, 0, 0), shield_button, 3) 

        # hoverr
        if can_upgrade:
            if farm_button.collidepoint(mouse_pos):
                hover_surface = pygame.Surface((50, 50))
                hover_surface.set_alpha(100)
                hover_surface.fill(HOVER_COLOR)
                screen.blit(hover_surface, (WIDTH + 20, 350))
                
            if turret_button.collidepoint(mouse_pos):
                hover_surface = pygame.Surface((50, 50))
                hover_surface.set_alpha(100)
                hover_surface.fill(HOVER_COLOR)
                screen.blit(hover_surface, (WIDTH + 75, 350))
                
            if shield_button.collidepoint(mouse_pos):
                hover_surface = pygame.Surface((50, 50))
                hover_surface.set_alpha(100)
                hover_surface.fill(HOVER_COLOR)
                screen.blit(hover_surface, (WIDTH + 130, 350))

    
        if can_upgrade:
            screen.blit(pygame.transform.scale(piece_images[f"{piece_color}_farm"], (50, 50)), (WIDTH + 20, 350))
            screen.blit(pygame.transform.scale(piece_images[f"{piece_color}_turret"], (50, 50)), (WIDTH + 75, 350))
            screen.blit(pygame.transform.scale(piece_images[f"{piece_color}_shield"], (50, 50)), (WIDTH + 130, 350))
        else:
         
            screen.blit(pygame.transform.scale(piece_images[f"{piece_color}_farm"], (50, 50)), (WIDTH + 20, 350))
            screen.blit(pygame.transform.scale(piece_images[f"{piece_color}_turret"], (50, 50)), (WIDTH + 75, 350))
            screen.blit(pygame.transform.scale(piece_images[f"{piece_color}_shield"], (50, 50)), (WIDTH + 130, 350))
            
           
            for button in [farm_button, turret_button, shield_button]:
                gray_overlay = pygame.Surface((50, 50))
                gray_overlay.set_alpha(130)
                gray_overlay.fill((200, 200, 200))
                screen.blit(gray_overlay, button)

        buttons.extend([farm_button, turret_button, shield_button])

        # Fire turret
        fire_turret_button = pygame.Rect(WIDTH + 20, 410, 160, 40)
        has_turret = game.board.has_turret(piece_color)
        
        # Checks if any turret has valid targets
        has_valid_targets = False
        if has_turret:
            for row in range(8):
                for col in range(8):
                    piece = game.board.get_piece_at(row, col)
                    if piece and piece.color == piece_color and piece.piece_type == PieceType.TURRET:
                        valid_targets = game.find_valid_targets_for_turret(row, col)
                        if valid_targets:
                            has_valid_targets = True
                            break
                if has_valid_targets:
                    break
        
        can_fire = has_actions and has_turret and not game.pawn_placement_mode and not game.upgrade_mode and has_valid_targets

        button_color = RED if can_fire else (200, 200, 200)
        pygame.draw.rect(screen, button_color, fire_turret_button)

        if fire_turret_button.collidepoint(mouse_pos) and can_fire:
            hover_surface = pygame.Surface((160, 40))
            hover_surface.set_alpha(100)
            hover_surface.fill(HOVER_COLOR)
            screen.blit(hover_surface, (WIDTH + 20, 410))

        if game.firing_mode:
            pygame.draw.rect(screen, (255, 255, 0), fire_turret_button, 3)
            
        fire_turret_text = font.render("Fire Turret", True, BLACK if can_fire else (120, 120, 120))
        screen.blit(fire_turret_text, (WIDTH + 40, 420))
        buttons.append(fire_turret_button)

        #buy actions
        buy_action_button = pygame.Rect(WIDTH + 20, 460, 160, 40)

        if game.action_points[piece_color] >= 3 and not game.pawn_placement_mode and not game.upgrade_mode and not game.firing_mode:
            # Active state - Gold background
            pygame.draw.rect(screen, GOLD, buy_action_button)
            buy_action_text = font.render("Buy Action", True, BLACK)
            
    
            if buy_action_button.collidepoint(mouse_pos) and not game.pawn_placement_mode and not game.upgrade_mode and not game.firing_mode:
                hover_surface = pygame.Surface((160, 40))
                hover_surface.set_alpha(100)
                hover_surface.fill(HOVER_COLOR)
                screen.blit(hover_surface, (WIDTH + 20, 460))
        else:
            pygame.draw.rect(screen, (200, 200, 200), buy_action_button)  
            
          
            buy_action_text = font.render("Buy Action", True, (120, 120, 120)) 

    
        screen.blit(buy_action_text, (WIDTH + 40, 470))
        buttons.append(buy_action_button)

        # Cancel
        cancel_button = pygame.Rect(WIDTH + 20, 510, 160, 40)

        if game.pawn_placement_mode or game.upgrade_mode or game.firing_mode:
            # Active state
            pygame.draw.rect(screen, (200, 180, 190), cancel_button)
            pygame.draw.rect(screen, BLACK, cancel_button, 3)
            cancel_text = font.render("Cancel", True, BLACK)
            
            if cancel_button.collidepoint(mouse_pos):
                hover_surface = pygame.Surface((160, 40))
                hover_surface.set_alpha(100)
                hover_surface.fill(HOVER_COLOR)
                screen.blit(hover_surface, (WIDTH + 20, 510))
        else:
           
            pygame.draw.rect(screen, (200, 200, 200), cancel_button)  
            cancel_text = font.render("Cancel", True, (120, 120, 120)) 

      
        screen.blit(cancel_text, (WIDTH + 40, 520))
        buttons.append(cancel_button)
        
        # Pass turn
        pass_turn_button = pygame.Rect(WIDTH + 20, 560, 160, 40)
        pygame.draw.rect(screen, (128, 128, 128), pass_turn_button)

        if pass_turn_button.collidepoint(mouse_pos):
  
            pygame.draw.rect(screen, (255, 215, 0), pass_turn_button, 3)  # Gold border to make more noticeable
            
            #big glow
            hover_surface = pygame.Surface((160, 40))
            hover_surface.set_alpha(150)  
            hover_surface.fill((255, 255, 150))  
            screen.blit(hover_surface, (WIDTH + 20, 560))
            
           
            pass_turn_text = font.render("Pass Turn", True, (50, 50, 50))  
        else:
            pass_turn_text = font.render("Pass Turn", True, BLACK)

        screen.blit(pass_turn_text, (WIDTH + 40, 570))
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
                    # Check if any turret has valid targets
                    piece_color = "white" if game.turn.lower().startswith("white") else "black"
                    has_valid_targets = False
                    for row in range(8):
                        for col in range(8):
                            piece = game.board.get_piece_at(row, col)
                            if piece and piece.color == piece_color and piece.piece_type == PieceType.TURRET:
                                valid_targets = game.find_valid_targets_for_turret(row, col)
                                if valid_targets:
                                    has_valid_targets = True
                                    break
                        if has_valid_targets:
                            break
                    
                    if has_valid_targets:
                        game.initiate_turret_firing()
            elif button == buttons[5]:  # Buy Action
                if not game.upgrade_mode and not game.firing_mode and not game.pawn_placement_mode:
                    game.buy_action()
            elif button == buttons[6]:  # Cancel
                game.cancel_action()
            elif button == buttons[7]:  # Pass Turn
                if game.upgrade_mode or game.firing_mode or game.pawn_placement_mode:
                    game.cancel_action()
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