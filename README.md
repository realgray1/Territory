# Territory – Q-Learning Board Game AI

Territory is a Python-based board game that integrates a reinforcement learning agent trained with **Q-Learning**. The AI evaluates previous game states and selects optimal moves based on the highest Q-values stored in a Q-table.

## Features

* **Reinforcement Learning:** Implements Q-Learning to iteratively improve decision-making.
* **Custom Training:** Run simulations to train the AI on game state/action pairs and update the Q-table.
* **Scalable Simulations:** Configure the number of training episodes to balance performance and accuracy.
* **Game Logging:** Game data is recorded after each run to support further analysis and model refinement.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/realgray1/territory.git
cd territory
pip install -r requirements.txt
```

## Usage

To play the game:

```bash
python main.py
```

To train the AI agent:

```bash
python train_q_learning_ai.py
```

By default, the agent runs 50 training games. You can adjust this by editing:

```python
if __name__ == "__main__":
    train_q_learning_ai(episodes=50)  # change 50 to desired number
```

## Notes

* Performance may degrade with very high numbers of simulations; it is recommended to balance accuracy with runtime.
* Works with Python 3.13 (earlier versions may not be supported).

---

