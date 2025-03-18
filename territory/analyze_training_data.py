import pandas as pd
import matplotlib.pyplot as plt

def analyze_training_data(file_name='game_data.csv'):
    # Read the CSV file
    data = pd.read_csv(file_name)

    # Convert 'turn' to numeric, coerce errors to NaN, and drop rows with NaN in 'turn'
    data['turn'] = pd.to_numeric(data['turn'], errors='coerce')
    data.dropna(subset=['turn'], inplace=True)

    # Calculate average reward per turn for each episode
    data['reward'] = pd.to_numeric(data['reward'], errors='coerce')
    data.dropna(subset=['reward'], inplace=True)
    
    average_reward_per_turn = data.groupby('episode').apply(lambda x: x['reward'].sum() / x['turn'].max())

    # Plot average reward per turn
    plt.figure(figsize=(10, 5))
    plt.plot(average_reward_per_turn.index, average_reward_per_turn.values, marker='o', linestyle='-')
    plt.xlabel('Episode')
    plt.ylabel('Average Reward per Turn')
    plt.title('Average Reward per Turn Over Episodes')
    plt.grid(True)
    plt.show()

    # Track wins for both colors individually
    wins_white = data[(data['outcome'] == 'win') & (data['winner'] == 'Player 1')].groupby('episode').size()
    wins_black = data[(data['outcome'] == 'win') & (data['winner'] == 'Player 2')].groupby('episode').size()

    # Plot wins for both colors
    plt.figure(figsize=(10, 5))
    plt.plot(wins_white.index, wins_white.values, marker='x', linestyle='-', color='b', label='White Wins (Player 1)')
    plt.plot(wins_black.index, wins_black.values, marker='x', linestyle='-', color='r', label='Black Wins (Player 2)')
    plt.xlabel('Episode')
    plt.ylabel('Number of Wins')
    plt.title('Number of Wins Over Episodes')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    analyze_training_data()