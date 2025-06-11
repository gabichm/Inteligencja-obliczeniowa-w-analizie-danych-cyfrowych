import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from pettingzoo.butterfly import cooperative_pong_v5

# 1. Tworzenie środowiska PettingZoo
env = cooperative_pong_v5.env()

# 2. Funkcja do konwersji środowiska PettingZoo na format Gymnasium
class PettingZooEnvWrapper(gym.Env):
    def __init__(self, pettingzoo_env):
        super().__init__()
        self.pettingzoo_env = pettingzoo_env

        # Resetuj środowisko, by ustawić pierwszy agent
        self.pettingzoo_env.reset()
        self.agent_name = self.pettingzoo_env.agents[0]

        # Ustaw observation_space i action_space od razu
        self.observation_space = self.pettingzoo_env.observation_space(self.agent_name)
        self.action_space = self.pettingzoo_env.action_space(self.agent_name)

        self.reward_range = (-float('inf'), float('inf'))
        self.spec = None

    def step(self, action):
        # Wykonaj akcję dla aktualnego agenta
        observation, reward, terminated, truncated, info = self.pettingzoo_env.last()

        if terminated or truncated:
            action = None

        self.pettingzoo_env.step(action)

        # Pobierz informacje dla wybranego agenta
        observation, reward, terminated, truncated, info = self.pettingzoo_env.last()

        done = terminated or truncated

        return observation, reward, done, False, info

    def reset(self, seed=None, options=None):
        self.pettingzoo_env.reset(seed=seed)
        self.agent_name = self.pettingzoo_env.agents[0]
        observation, reward, terminated, truncated, info = self.pettingzoo_env.last()
        return observation, {}

    def render(self, mode='human'):
        return self.pettingzoo_env.render(mode)

    def close(self):
        self.pettingzoo_env.close()


# Konwertuj środowisko PettingZoo na format Gymnasium
gym_env = PettingZooEnvWrapper(env)

# 3. Definiowanie hiperparametrów dla agentów
hyperparams_agent1 = {
    "learning_rate": 0.0005,
    "gamma": 0.99,
    "batch_size": 64,
}

hyperparams_agent2 = {
    "learning_rate": 0.0003,
    "gamma": 0.95,
    "batch_size": 32,
}

# 4. Tworzenie modeli PPO dla agentów
model_agent1 = PPO("MlpPolicy", gym_env, verbose=0, **hyperparams_agent1)
model_agent2 = PPO("MlpPolicy", gym_env, verbose=0, **hyperparams_agent2)

# 5. Uczenie modeli
num_episodes = 100
rewards_agent1 = []
rewards_agent2 = []

for episode in range(num_episodes):
    obs, _ = gym_env.reset()
    total_reward_agent1 = 0
    total_reward_agent2 = 0
    done = False

    while not done:
        action_agent1, _ = model_agent1.predict(obs, deterministic=True)
        action_agent2, _ = model_agent2.predict(obs, deterministic=True)

        # Wykonaj akcje w środowisku
        obs, reward, done, _, info = gym_env.step(action_agent1)

        total_reward_agent1 += reward
        total_reward_agent2 += reward  # Zakładamy, że obaj agenci otrzymują tę samą nagrodę

    rewards_agent1.append(total_reward_agent1)
    rewards_agent2.append(total_reward_agent2)

    print(f"Episode: {episode + 1}, Reward Agent 1: {total_reward_agent1}, Reward Agent 2: {total_reward_agent2}")

# 6. Tworzenie wykresu
plt.plot(rewards_agent2, label="Agent 2")
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("Reward per Episode for Each Agent")
plt.legend()
plt.savefig("nag.png") 