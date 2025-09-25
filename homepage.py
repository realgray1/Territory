import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Territory Game - Home")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

rules_text = ("The game is played on a chess board and starts with each player placing their king and a farm wherever they want on the board, "
              "except the center 4 tiles. White goes first followed by black, after this initial phase white goes first."
              "On your turn you get 1 free action to do, which can be spent placing a pawn, upgrading a pawn to one of 3 pieces (turrets, farms, shields), "
              "or firing a turret at a piece."
              "Pawns must be placed next to one of your existing pieces, if at any point a piece of yours becomes isolated from the king's island (after a turret fires) "
              "it gets immediately destroyed."
              "Each farm a player has at the end of their turn gives them one action point, and 3 action points can be traded in on your turn for more actions. Black starts game with an extra Action Point. "
              "Turrets fire diagonally and can only hit enemy pieces in their line of sight. Enemy turrets, farms, and pawns get destroyed in one hit. "
              "Shields will revert to pawns upon being hit. If you hit the enemy king, you win")

def draw_background():
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    for y in range(screen_height):
        # Gradient
        color = (255, max(0, 255 - y // 3), max(0, 255 - y // 3))
        pygame.draw.line(screen, color, (0, y), (screen_width, y))

def draw_home_page(mouse_pos):
    screen.fill(WHITE)
    draw_background()

    # Gets the actual screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Draw title
    title_text = font.render("Welcome to Territory", True, BLACK)
    title_x = (screen_width - title_text.get_width()) // 2
    title_y = screen_height // 4
    screen.blit(title_text, (title_x, title_y))

    # Buttons
    button_width, button_height = 200, 50
    button_x = (screen_width - button_width) // 2 

    play_side_by_side_button = pygame.Rect(button_x, screen_height // 2 - 60, button_width, button_height)
    play_vs_ai_button = pygame.Rect(button_x, screen_height // 2 + 20, button_width, button_height)
    how_to_play_button = pygame.Rect(button_x, screen_height // 2 + 100, button_width, button_height)

    side_by_side_hover = play_side_by_side_button.collidepoint(mouse_pos)
    play_vs_ai_hover = play_vs_ai_button.collidepoint(mouse_pos)
    how_to_play_hover = how_to_play_button.collidepoint(mouse_pos)

    pygame.draw.rect(screen, LIGHT_GRAY if side_by_side_hover else GRAY, play_side_by_side_button, border_radius=10)
    pygame.draw.rect(screen, LIGHT_GRAY if play_vs_ai_hover else GRAY, play_vs_ai_button, border_radius=10)
    pygame.draw.rect(screen, LIGHT_GRAY if how_to_play_hover else GRAY, how_to_play_button, border_radius=10)

    play_side_by_side_text = font.render("Play Human", True, BLACK)
    play_vs_ai_text = font.render("Play vs AI", True, BLACK)
    how_to_play_text = font.render("How to Play", True, BLACK)

    # This centers the text
    screen.blit(play_side_by_side_text, (play_side_by_side_button.centerx - play_side_by_side_text.get_width() // 2,
                                        play_side_by_side_button.centery - play_side_by_side_text.get_height() // 2))
    
    screen.blit(play_vs_ai_text, (play_vs_ai_button.centerx - play_vs_ai_text.get_width() // 2,
                                play_vs_ai_button.centery - play_vs_ai_text.get_height() // 2))
    
    screen.blit(how_to_play_text, (how_to_play_button.centerx - how_to_play_text.get_width() // 2,
                                how_to_play_button.centery - how_to_play_text.get_height() // 2))
    
    # Add attribution text in the bottom corner
    attribution_font = pygame.font.SysFont('Arial', 18)  # Smaller font for attribution
    attribution_text = attribution_font.render("Dean Carpenter", True, BLACK)
    attribution_x = screen_width - attribution_text.get_width() - 10  # 10 pixels from right edge
    attribution_y = screen_height - attribution_text.get_height() - 10  # 10 pixels from bottom edge
    screen.blit(attribution_text, (attribution_x, attribution_y))

    return play_side_by_side_button, play_vs_ai_button, how_to_play_button


def draw_rules_overlay(screen, rules_text):
    # Create semi-transparent overlay for the background
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Darker, more opaque overlay
    screen.blit(overlay, (0, 0))
    
    # Define popup dimensions
    screen_width, screen_height = screen.get_size()
    popup_width = screen_width * 0.8
    popup_height = screen_height * 0.8
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    
    # Draw popup background
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, (245, 245, 245), popup_rect, border_radius=15)
    pygame.draw.rect(screen, (200, 200, 200), popup_rect, width=2, border_radius=15)  # Border
    
    # Draw title
    title_font = pygame.font.SysFont('Arial', 32, bold=True)
    title_text = title_font.render("Game Rules", True, (50, 50, 50))
    title_x = popup_x + (popup_width - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, popup_y + 20))
    
    # Draw separator line
    pygame.draw.line(screen, (200, 200, 200), 
                    (popup_x + 30, popup_y + 60), 
                    (popup_x + popup_width - 30, popup_y + 60), 
                    2)
    
    # Close button (X)
    close_size = 30
    close_rect = pygame.Rect(popup_x + popup_width - close_size - 15, popup_y + 15, close_size, close_size)
    pygame.draw.rect(screen, (220, 80, 80), close_rect, border_radius=15)
    x_font = pygame.font.SysFont('Arial', 20, bold=True)
    x_text = x_font.render("X", True, (255, 255, 255))
    screen.blit(x_text, (close_rect.centerx - x_text.get_width()//2, 
                         close_rect.centery - x_text.get_height()//2))
    
    # Use a smaller font size for the rules text
    rules_font = pygame.font.SysFont('Arial', 19)  # Reduced from 24 to 18
    
    # Render rules text with proper wrapping
    text_area_width = popup_width - 60  # Margin on both sides
    text_x = popup_x + 30
    text_y = popup_y + 80
    
    # Split text into paragraphs
    paragraphs = rules_text.split('.')
    
    # For each paragraph, handle word wrapping
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue  # Skip empty paragraphs
            
        paragraph = paragraph.strip() + "."
        words = paragraph.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width = rules_font.size(test_line)[0]
            
            if test_width <= text_area_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Render each line
        for line in lines:
            text_surface = rules_font.render(line, True, (50, 50, 50))
            screen.blit(text_surface, (text_x, text_y))
            text_y += rules_font.get_linesize()
        
        # Add space between paragraphs
        text_y += 8  # Slightly reduced paragraph spacing
    
    return close_rect  # Return the close button rect for event handling

def home_page():
    show_rules = False
    close_button = None
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Only redraw the home page if we're not showing rules
        if not show_rules:
            play_side_by_side_button, play_vs_ai_button, how_to_play_button = draw_home_page(mouse_pos)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_rules and close_button and close_button.collidepoint(event.pos):
                    show_rules = False
                elif not show_rules:
                    if play_side_by_side_button.collidepoint(event.pos):
                        print("Local Play button clicked")
                        return "side_by_side"
                    elif play_vs_ai_button.collidepoint(event.pos):
                        print("Play vs AI button clicked")
                        return "play_vs_ai"
                    elif how_to_play_button.collidepoint(event.pos):
                        print("How to Play button clicked")
                        show_rules = True
        
        # Draw rules overlay if needed
        if show_rules:
            close_button = draw_rules_overlay(screen, rules_text)
        
        pygame.display.flip()