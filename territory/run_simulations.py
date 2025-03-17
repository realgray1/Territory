from ai_game.ai_logic import Game
from ai_game.simple_ai import SimpleAI
from ai_game.data_collection import DataCollector

def run_single_game():
    data_collector = DataCollector()
    game = Game()
    ai_player1 = SimpleAI(game, player_name="Player 1")
    ai_player2 = SimpleAI(game, player_name="Player 2")
    
    game_over = False

    while not game_over:
        ai_player1.make_move()
        if game.game_over:
            data_collector.log_data(
                data_collector.serialize_game_state(game),
                {'action': 'game_over', 'winner': game.winner},
                'win' if game.winner == 'Player 1' else 'loss'
            )
            data_collector.log_game_end()  # Log the end of the game
            game_over = True
            break

        ai_player2.make_move()
        if game.game_over:
            data_collector.log_data(
                data_collector.serialize_game_state(game),
                {'action': 'game_over', 'winner': game.winner},
                'win' if game.winner == 'Player 2' else 'loss'
            )
            data_collector.log_game_end()  # Log the end of the game
            game_over = True

if __name__ == "__main__":
    run_single_game()