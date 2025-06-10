from pettingzoo.mpe import simple_spread_v3
import supersuit as ss
from stable_baselines3 import PPO
import numpy as np
import matplotlib.pyplot as plt
from torch.nn import ReLU
import gym


def make_single_agent_env(agent_id):
    """
    Tworzy środowisko PettingZoo, ale zwraca obserwacje i nagrody tylko dla jednego agenta,
    by móc trenować go niezależnie. Wrapper dziedziczy po gym.Env, co jest wymagane przez SB3.
    """
    env = simple_spread_v3.env(N=2, local_ratio=0.5, max_cycles=50, continuous_actions=False)
    env.reset()

    from pettingzoo.utils.conversions import aec_to_parallel
    env = aec_to_parallel(env)

    class SingleAgentWrapper(gym.Env):
        def __init__(self, env, agent_id):
            super().__init__()
            self.env = env
            self.agent_id = agent_id
            self.agents = env.agents  # lista agentów

            self.action_space = env.action_space(agent_id)
            self.observation_space = env.observation_space(agent_id)

        def reset(self):
            obs = self.env.reset()
            return obs[self.agent_id]

        def step(self, action):
            actions = {}
            for a in self.agents:
                if a == self.agent_id:
                    actions[a] = action
                else:
                    actions[a] = self.env.action_space(a).sample()

            obs, rewards, dones, infos = self.env.step(actions)

            return obs[self.agent_id], rewards[self.agent_id], dones[self.agent_id], infos[self.agent_id]

        def render(self, mode="human"):
            return self.env.render(mode=mode)

        def close(self):
            self.env.close()

    return SingleAgentWrapper(env, agent_id)


# Tworzymy dwa osobne środowiska dla agentów
env_agent1 = make_single_agent_env("agent_0")
env_agent2 = make_single_agent_env("agent_1")

# Konfiguracja PPO osobno dla każdego agenta
model_agent1 = PPO(
    "MlpPolicy",
    env_agent1,
    verbose=1,
    learning_rate=3e-4,
    n_steps=4096,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    clip_range=0.2,
    policy_kwargs=dict(net_arch=[256, 256], activation_fn=ReLU)
)

model_agent2 = PPO(
    "MlpPolicy",
    env_agent2,
    verbose=1,
    learning_rate=3e-4,
    n_steps=4096,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    clip_range=0.2,
    policy_kwargs=dict(net_arch=[256, 256], activation_fn=ReLU)
)

# Tablice na wyniki
mean_rewards_agent1 = []
mean_rewards_agent2 = []
max_rewards_agent1 = []
max_rewards_agent2 = []

num_episodes = 100
episode_length = 25  # liczba kroków w epizodzie

for ep in range(num_episodes):
    # Trenujemy oba modele osobno (2000 kroków każdy)
    model_agent1.learn(total_timesteps=2000, reset_num_timesteps=False)
    model_agent2.learn(total_timesteps=2000, reset_num_timesteps=False)

    obs1 = env_agent1.reset()
    obs2 = env_agent2.reset()

    rewards_ep_agent1 = []
    rewards_ep_agent2 = []

    for _ in range(episode_length):
        action1, _ = model_agent1.predict(obs1, deterministic=True)
        obs1, reward1, done1, _ = env_agent1.step(action1)
        rewards_ep_agent1.append(reward1)

        action2, _ = model_agent2.predict(obs2, deterministic=True)
        obs2, reward2, done2, _ = env_agent2.step(action2)
        rewards_ep_agent2.append(reward2)

        if done1 or done2:
            break

    mean_r1 = np.mean(rewards_ep_agent1)
    max_r1 = np.max(rewards_ep_agent1)
    mean_r2 = np.mean(rewards_ep_agent2)
    max_r2 = np.max(rewards_ep_agent2)

    mean_rewards_agent1.append(mean_r1)
    max_rewards_agent1.append(max_r1)
    mean_rewards_agent2.append(mean_r2)
    max_rewards_agent2.append(max_r2)

    print(
        f"Epizod {ep+1} - Agent 1: średnia nagroda {mean_r1:.3f}, max nagroda {max_r1:.3f} | "
        f"Agent 2: średnia nagroda {mean_r2:.3f}, max nagroda {max_r2:.3f}"
    )

# Zapisujemy modele
model_agent1.save("ppo_agent1_simple_spread")
model_agent2.save("ppo_agent2_simple_spread")

# Rysujemy wykresy
plt.figure(figsize=(12, 6))
plt.plot(mean_rewards_agent1, label="Średnia nagroda - Agent 1")
plt.plot(mean_rewards_agent2, label="Średnia nagroda - Agent 2")
plt.xlabel("Epizod")
plt.ylabel("Średnia nagroda")
plt.title("PPO: Średnia nagroda dla każdego agenta")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("ppo_mean_rewards_per_agent.png")


plt.figure(figsize=(12, 6))
plt.plot(max_rewards_agent1, label="Maksymalna nagroda - Agent 1", linestyle="--")
plt.plot(max_rewards_agent2, label="Maksymalna nagroda - Agent 2", linestyle="--")
plt.xlabel("Epizod")
plt.ylabel("Maksymalna nagroda")
plt.title("PPO: Maksymalna nagroda dla każdego agenta")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("ppo_max_rewards_per_agent.png")
