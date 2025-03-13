import homepage
import game.display as display  # Human gameplay display module
import ai_game.ai_display as ai_display  # AI gameplay display module
import pygame

def main():
    selected_mode = homepage.home_page()
    print(f"Selected mode: {selected_mode}")

    if selected_mode == "side_by_side":
        pygame.display.set_caption('Territory - Play Side by Side')
        display.start_game_display()  # Start the side-by-side game mode
    elif selected_mode == "play_vs_ai":
        pygame.display.set_caption('Territory - Play vs AI')
        ai_display.start_game_display()  # Start the AI game mode

if __name__ == "__main__":
    main()