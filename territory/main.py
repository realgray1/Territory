import homepage
import game.display as display  # Human gameplay display module
import pygame
from ai_game.ai_display import start_ai_game_display  # Import the AI game display function

def main():
    selected_mode = homepage.home_page()
    print(f"Selected mode: {selected_mode}")

    if selected_mode == "side_by_side":
        pygame.display.set_caption('Territory - Play Side by Side')
        display.start_game_display()
    elif selected_mode == "play_vs_ai":
        pygame.display.set_caption('Territory - Play vs AI')
        start_ai_game_display()  # Run the AI game display

if __name__ == "__main__":
    main()