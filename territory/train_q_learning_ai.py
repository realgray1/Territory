import pickle
from ai_game.ai_logic import Game
from ai_game.q_learning_ai import QLearningAI
from ai_game.data_collection import DataCollector

def save_q_table(q_table, file_name='qtable/q_table.pkl'):
    with open(file_name, 'wb') as file:
        pickle.dump(q_table, file)
    print("Q-table saved.")

def load_q_table(file_name='qtable/q_table.pkl'):
    try:
        with open(file_name, 'rb') as file:
            q_table = pickle.load(file)
        print("Q-table loaded.")
        return q_table
    except FileNotFoundError:
        print("Q-table file not found. Starting with an empty Q-table.")
        return {}

def train_q_learning_ai(episodes=50, max_turns=100):
    q_table = load_q_table()
    
    for episode in range(episodes):
        print(f"Starting episode {episode + 1}/{episodes}")
        data_collector = DataCollector()
        game = Game()
        ai_player1 = QLearningAI(game, player_name="Player 1", episode=episode + 1)
        ai_player2 = QLearningAI(game, player_name="Player 2", episode=episode + 1)
        
        ai_player1.q_table = q_table
        ai_player2.q_table = q_table
        
        game_over = False
        turn_count = 0
        state_history = set()

        while not game_over and turn_count < max_turns:
            #Main game loop
            turn_count += 1
            current_state = ai_player1.get_state()
            ai_player1.make_move()
            if game.game_over:
                print(f"Game over! Winner: {game.winner}")
                game_over = True
                break

            ai_player2.make_move()
            if game.game_over:
                print(f"Game over! Winner: {game.winner}")
                game_over = True
                break

        # Epsilon decay for q learning and decision making
        ai_player1.epsilon = max(ai_player1.min_epsilon, ai_player1.epsilon * ai_player1.epsilon_decay)
        ai_player2.epsilon = max(ai_player2.min_epsilon, ai_player2.epsilon * ai_player2.epsilon_decay)
        
        print(f"Episode {episode + 1}/{episodes} completed in {turn_count} turns\n")

    save_q_table(ai_player1.q_table) # WE NEED THIS LINE TO SAVE THE Q TABLE

if __name__ == "__main__":
    train_q_learning_ai(episodes=50)  # Adjust number of episodes as needed --- NUMBERS > 1000 WILL TAKE A WHILE, ANYTHING MORE THAN 10k WILL MAKE THE Q TABLE FILE HUGE AND SLOW