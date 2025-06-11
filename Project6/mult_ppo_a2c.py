import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

from pettingzoo.butterfly import cooperative_pong_v5
import supersuit as ss

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# --- Wrapper dla pojedynczego agenta (z PettingZoo do Gym)
class SingleAgentWrapper(gym.Env):
    def __init__(self, pettingzoo_env, agent_name):
        super().__init__()
        self.env = pettingzoo_env
        self.agent = agent_name

        self.env.reset()
        self.observation_space = self.env.observation_space(self.agent)
        self.action_space = self.env.action_space(self.agent)
        self._done = False

    def reset(self, **kwargs):
        self.env.reset()
        self._done = False
        obs, _, terminated, truncated, _ = self.env.last()
        return obs, {}


    def step(self, action):
        if self._done:
            # jeśli done, nie wykonuj akcji
            return None, 0, True, False, {}

        # Wykonaj krok tylko dla konkretnego agenta
        # Trzeba iterować w pętli, by przejść do aktualnego agenta
        while True:
            current_agent = self.env.agent_selection
            if current_agent == self.agent:
                self.env.step(action)
                break
            else:
                self.env.step(None)

        obs, reward, terminated, truncated, info = self.env.last()
        self._done = terminated or truncated
        return obs, reward, self._done, False, info

    def render(self, mode='human'):
        return self.env.render(mode=mode)

    def close(self):
        self.env.close()

# --- Tworzymy środowisko PettingZoo z przetworzeniem
env = cooperative_pong_v5.env()
env = ss.color_reduction_v0(env, mode='B')
env = ss.resize_v1(env, 84, 84)
env = ss.frame_stack_v1(env, 4)

# --- Wrappery dla agentów (upewnij się co do nazw agentów w env.agents)
agent_names = env.possible_agents  # np. ['first_0', 'first_1']

agent0_env = SingleAgentWrapper(env, agent_names[0])
agent1_env = SingleAgentWrapper(env, agent_names[1])

# --- Opakowujemy w DummyVecEnv - wymagane przez SB3
vec_env0 = DummyVecEnv([lambda: agent0_env])
vec_env1 = DummyVecEnv([lambda: agent1_env])

# --- Definicja modeli PPO dla każdego agenta z różnymi hiperparametrami
model_agent0 = PPO("CnnPolicy", vec_env0, learning_rate=0.0005, gamma=0.99, verbose=1)
model_agent1 = PPO("CnnPolicy", vec_env1, learning_rate=0.0003, gamma=0.95, verbose=1)

# --- Trening
num_episodes = 100
rewards_agent0 = []
rewards_agent1 = []

for episode in range(num_episodes):
    obs0 = vec_env0.reset()
    obs1 = vec_env1.reset()

    done0 = False
    done1 = False

    total_reward0 = 0
    total_reward1 = 0

    while not (done0 and done1):
        action0, _ = model_agent0.predict(obs0, deterministic=False)
        obs0, reward0, done0, _ = vec_env0.step(action0)
        total_reward0 += reward0[0]

        action1, _ = model_agent1.predict(obs1, deterministic=False)
        obs1, reward1, done1, _ = vec_env1.step(action1)
        total_reward1 += reward1[0]

        # Możesz tutaj dodać model_agentX.learn() jeśli chcesz online train, 
        # albo robić learn() po epizodzie

    # Po epizodzie ucz modele
    model_agent0.learn(total_timesteps=2048, reset_num_timesteps=False)
    model_agent1.learn(total_timesteps=2048, reset_num_timesteps=False)

    rewards_agent0.append(total_reward0)
    rewards_agent1.append(total_reward1)

    print(f"Episode {episode+1} | Agent0 reward: {total_reward0:.2f} | Agent1 reward: {total_reward1:.2f}")

# --- Rysujemy wykres
plt.plot(rewards_agent0, label="Agent 0")
plt.plot(rewards_agent1, label="Agent 1")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.title("Training Rewards per Agent")
plt.legend()
plt.grid()
plt.savefig("pl.png")


