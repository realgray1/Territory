import pickle
from ai_game.ai_logic import Game
from ai_game.q_learning_ai import QLearningAI  # Import the Q-learning AI
from ai_game.data_collection import DataCollector

def save_q_table(q_table, file_name='q_table.pkl'):
    with open(file_name, 'wb') as file:
        pickle.dump(q_table, file)
    print("Q-table saved.")

def load_q_table(file_name='q_table.pkl'):
    try:
        with open(file_name, 'rb') as file:
            q_table = pickle.load(file)
        print("Q-table loaded.")
        return q_table
    except FileNotFoundError:
        print("Q-table file not found. Starting with an empty Q-table.")
        return {}

def train_q_learning_ai(episodes=50):
    # Load existing Q-table if available
    q_table = load_q_table()
    
    for episode in range(episodes):
        print(f"Starting episode {episode + 1}/{episodes}")
        data_collector = DataCollector()
        game = Game()
        ai_player1 = QLearningAI(game, player_name="Player 1", episode=episode + 1)
        ai_player2 = QLearningAI(game, player_name="Player 2", episode=episode + 1)
        
        # Set the loaded Q-table to both AI players
        ai_player1.q_table = q_table
        ai_player2.q_table = q_table
        
        game_over = False

        while not game_over:
            ai_player1.make_move()
            if game.game_over:
                print(f"Game over! Winner: {game.winner}")
                break

            ai_player2.make_move()
            if game.game_over:
                print(f"Game over! Winner: {game.winner}")
                break

        # Decay epsilon for both AI players
        ai_player1.epsilon = max(ai_player1.min_epsilon, ai_player1.epsilon * ai_player1.epsilon_decay)
        ai_player2.epsilon = max(ai_player2.min_epsilon, ai_player2.epsilon * ai_player2.epsilon_decay)
        
        print(f"Episode {episode + 1}/{episodes} completed\n")

    # Save the Q-table after training
    save_q_table(ai_player1.q_table)

if __name__ == "__main__":
    train_q_learning_ai(episodes=50)  # Adjust number of episodes as needed