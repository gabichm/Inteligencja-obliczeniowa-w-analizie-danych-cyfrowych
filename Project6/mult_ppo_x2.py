from pettingzoo.mpe import simple_spread_v3
from stable_baselines3 import PPO
import numpy as np
import matplotlib.pyplot as plt
from torch.nn import ReLU
import gymnasium as gym

def make_single_agent_env(env, agent_id):
    """
    Wrapper tworzący środowisko single-agent dla wybranego agenta
    """
    class SingleAgentWrapper(gym.Env):
        def __init__(self, env, agent_id):
            super().__init__()
            self.env = env
            self.agent_id = agent_id

            # Pobieramy przestrzenie akcji i obserwacji dla wybranego agenta
            self.action_space = env.action_space(agent_id)
            self.observation_space = env.observation_space(agent_id)

            # Inicjalizacja środowiska
            self.env.reset()

        def reset(self, **kwargs):
            self.env.reset()
            obs, reward, terminated, truncated, info = self.env.last()
            return obs, {}

        def step(self, action):
            self.env.step(action)
            obs, reward, terminated, truncated, info = self.env.last()
            done = terminated or truncated
            return obs, reward, done, False, info

        def render(self, mode="human"):
            return self.env.render(mode=mode)

        def close(self):
            self.env.close()

    return SingleAgentWrapper(env, agent_id)

# Główne środowisko
env = simple_spread_v3.env(N=2, local_ratio=0.5, max_cycles=50, continuous_actions=False)

# Tworzymy wrappery dla każdego agenta
env_agent1 = make_single_agent_env(env, "agent_0")
env_agent2 = make_single_agent_env(env, "agent_1")

# Konfiguracja PPO
def make_model(env):
    return PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        clip_range=0.2,
        policy_kwargs=dict(net_arch=dict(pi=[64, 64], vf=[64, 64]), activation_fn=ReLU),
        device="cpu"
    )

model_agent1 = make_model(env_agent1)
model_agent2 = make_model(env_agent2)

# Trening i testowanie
num_episodes = 100
episode_length = 50  # Dopasowane do max_cycles

rewards_history = {"agent_0": [], "agent_1": []}

for ep in range(num_episodes):
    # Trening każdego agenta
    model_agent1.learn(total_timesteps=episode_length, reset_num_timesteps=False)
    model_agent2.learn(total_timesteps=episode_length, reset_num_timesteps=False)

    # Testowanie
    env.reset()
    episode_rewards = {agent: 0 for agent in env.agents}

    for agent in env.agent_iter():
        obs, reward, terminated, truncated, info = env.last()
        done_agent = terminated or truncated
        episode_rewards[agent] += reward

        if done_agent:
            action = None
        else:
            if agent == "agent_0":
                action, _ = model_agent1.predict(obs, deterministic=True)
            else:
                action, _ = model_agent2.predict(obs, deterministic=True)

        env.step(action)

    # Zapis wyników z bieżącego epizodu
    for agent in env.agents:
        rewards_history[agent].append(episode_rewards[agent])

    # Wypisanie statystyk
    for agent in env.agents:
        mean_reward = np.mean(rewards_history[agent])
        max_reward = np.max(rewards_history[agent])
        print(f"Epizod {ep+1} - {agent}: mean_reward={mean_reward:.2f}, max_reward={max_reward:.2f}")

    print(f"Epizod {ep+1}: Agent 0 - {episode_rewards['agent_0']:.2f}, Agent 1 - {episode_rewards['agent_1']:.2f}")

# Zapis modeli
model_agent1.save("ppo_agent1_simple_spread_fixed")
model_agent2.save("ppo_agent2_simple_spread_fixed")

# Wykresy
plt.figure(figsize=(12, 6))
plt.plot(rewards_history["agent_0"], label="Agent 0")
plt.plot(rewards_history["agent_1"], label="Agent 1")
plt.xlabel("Epizod")
plt.ylabel("Łączna nagroda")
plt.title("PPO: Nagrody w środowisku simple_spread")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("ppo_rewards_fixed.png")

