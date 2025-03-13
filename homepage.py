import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Territory Game - Home")  # Ensure caption remains consistent on the homepage

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont('Arial', 36)

# Buttons
play_side_by_side_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
play_vs_ai_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

def draw_home_page():
    screen.fill(WHITE)

    # Draw title
    title_text = font.render("Territory Game", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    # Draw buttons
    pygame.draw.rect(screen, GRAY, play_side_by_side_button)
    pygame.draw.rect(screen, GRAY, play_vs_ai_button)

    play_side_by_side_text = font.render("Play Side by Side", True, BLACK)
    play_vs_ai_text = font.render("Play vs AI", True, BLACK)

    screen.blit(play_side_by_side_text, (WIDTH // 2 - play_side_by_side_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(play_vs_ai_text, (WIDTH // 2 - play_vs_ai_text.get_width() // 2, HEIGHT // 2 + 30))

def home_page():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_side_by_side_button.collidepoint(event.pos):
                    print("Play Side by Side button clicked")
                    return "side_by_side"
                elif play_vs_ai_button.collidepoint(event.pos):
                    print("Play vs AI button clicked")
                    return "play_vs_ai"

        draw_home_page()
        pygame.display.flip()