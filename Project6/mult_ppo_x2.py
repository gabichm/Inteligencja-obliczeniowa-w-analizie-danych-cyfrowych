import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
import matplotlib.pyplot as plt

# 1. Definicja środowiska Connect Four
class ConnectFourEnv(gym.Env):
    def __init__(self, width=7, height=6):
        super(ConnectFourEnv, self).__init__()
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=int)
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(height, width), dtype=np.int32)
        self.action_space = gym.spaces.Discrete(width)
        self.current_player = 1  # 1 or -1

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.current_player = 1
        info = {}
        return self.board, info

    def step(self, action):
        # Sprawdzenie czy ruch jest poprawny
        if self.board[0, action] != 0:
            return self.board, -1, True, False, {}  # Niepoprawny ruch, kara

        # Wykonanie ruchu
        for i in range(self.height - 1, -1, -1):
            if self.board[i, action] == 0:
                self.board[i, action] = self.current_player
                break

        # Sprawdzenie czy ktoś wygrał
        winner = self.check_winner()
        done = winner != 0 or np.all(self.board != 0)
        reward = 1 if winner == self.current_player else 0

        # Zmiana gracza
        self.current_player *= -1

        return self.board, reward, done, False, {}

    def check_winner(self):
        # Implementacja sprawdzania wygranej (poziomo, pionowo, po skosie)
        # Uproszczona wersja - tylko poziomo
        for i in range(self.height):
            for j in range(self.width - 3):
                if (self.board[i, j] == self.board[i, j+1] == self.board[i, j+2] == self.board[i, j+3] != 0):
                    return self.board[i, j]

        # Sprawdzenie pionowo
        for i in range(self.height - 3):
            for j in range(self.width):
                if (self.board[i, j] == self.board[i+1, j] == self.board[i+2, j] == self.board[i+3, j] != 0):
                    return self.board[i, j]

        # Sprawdzenie po skosie (od lewej do prawej)
        for i in range(self.height - 3):
            for j in range(self.width - 3):
                if (self.board[i, j] == self.board[i+1, j+1] == self.board[i+2, j+2] == self.board[i+3, j+3] != 0):
                    return self.board[i, j]

        # Sprawdzenie po skosie (od prawej do lewej)
        for i in range(self.height - 3):
            for j in range(3, self.width):
                if (self.board[i, j] == self.board[i+1, j-1] == self.board[i+2, j-2] == self.board[i+3, j-3] != 0):
                    return self.board[i, j]

        return 0

# 2. Definicja hiperparametrów dla agentów
learning_rates = [0.0001, 0.0003, 0.001]
gammas = [0.95, 0.99]
clip_ranges = [0.1, 0.2]

# Wybierz hiperparametry dla agenta 1
lr1 = learning_rates[0]
gamma1 = gammas[0]
clip_range1 = clip_ranges[0]

# Wybierz hiperparametry dla agenta 2
lr2 = learning_rates[1]
gamma2 = gammas[1]
clip_range2 = clip_ranges[1]

# 3. Tworzenie agentów
env = ConnectFourEnv()
agent1 = {
    "model": PPO("MlpPolicy", env, learning_rate=lr1, gamma=gamma1, clip_range=clip_range1, verbose=0),
    "results": [],
    "label": f"Agent 1: LR={lr1}, Gamma={gamma1}, Clip={clip_range1}"
}
agent2 = {
    "model": PPO("MlpPolicy", env, learning_rate=lr2, gamma=gamma2, clip_range=clip_range2, verbose=0),
    "results": [],
    "label": f"Agent 2: LR={lr2}, Gamma={gamma2}, Clip={clip_range2}"
}

agents = [agent1, agent2]

# 4. Uczenie agentów
num_episodes = 1000

for episode in range(num_episodes):
    obs, _ = env.reset()
    done = False
    total_reward_agent1 = 0
    total_reward_agent2 = 0
    current_player = 0  # 0 dla agenta1, 1 dla agenta2

    while not done:
        action, _states = agents[current_player]["model"].predict(obs, deterministic=True)
        obs, reward, done, _, info = env.step(action)

        if current_player == 0:
            total_reward_agent1 += reward
            total_reward_agent2 -= reward
        else:
            total_reward_agent2 += reward
            total_reward_agent1 -= reward

        current_player = 1 - current_player  # Zmiana gracza

    agent1["results"].append(total_reward_agent1)
    agent2["results"].append(total_reward_agent2)
    agent1["model"].learn(total_timesteps=1)
    agent2["model"].learn(total_timesteps=1)

    # Wyświetlanie wyników po każdym epizodzie (opcjonalne)
    print(f"Epizod: {episode + 1}")
    print(f"  {agent1['label']}, Reward={agent1['results'][-1]}")
    print(f"  {agent2['label']}, Reward={agent2['results'][-1]}")

# 5. Analiza i Wykres
plt.figure(figsize=(12, 6))
episodes = range(1, num_episodes + 1)

plt.plot(episodes, agent1["results"], label=agent1["label"])
plt.plot(episodes, agent2["results"], label=agent2["label"])

# Dodanie etykiet i tytułu
plt.xlabel("Epizod")
plt.ylabel("Nagroda")
plt.title("Porównanie Agentów PPO w Connect Four")
plt.legend()
plt.grid(True)

# Wyświetlenie wykresu
plt.savefig("wyk.png")


