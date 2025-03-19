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

def draw_background():
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    for y in range(screen_height):
        #gradient
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

    side_by_side_hover = play_side_by_side_button.collidepoint(mouse_pos)
    play_vs_ai_hover = play_vs_ai_button.collidepoint(mouse_pos)

    pygame.draw.rect(screen, LIGHT_GRAY if side_by_side_hover else GRAY, play_side_by_side_button, border_radius=10)
    pygame.draw.rect(screen, LIGHT_GRAY if play_vs_ai_hover else GRAY, play_vs_ai_button, border_radius=10)

    play_side_by_side_text = font.render("Play Human", True, BLACK)
    play_vs_ai_text = font.render("Play vs AI", True, BLACK)

    #this centers the text
    screen.blit(play_side_by_side_text, (play_side_by_side_button.centerx - play_side_by_side_text.get_width() // 2,
                                         play_side_by_side_button.centery - play_side_by_side_text.get_height() // 2))
    
    screen.blit(play_vs_ai_text, (play_vs_ai_button.centerx - play_vs_ai_text.get_width() // 2,
                                  play_vs_ai_button.centery - play_vs_ai_text.get_height() // 2))

    return play_side_by_side_button, play_vs_ai_button

def home_page():
    while True:
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position
        play_side_by_side_button, play_vs_ai_button = draw_home_page(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_side_by_side_button.collidepoint(event.pos):
                    print("Play Human button clicked")
                    return "side_by_side"
                elif play_vs_ai_button.collidepoint(event.pos):
                    print("Play vs AI button clicked")
                    return "play_vs_ai"

        pygame.display.flip() 