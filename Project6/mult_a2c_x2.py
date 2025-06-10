from pettingzoo.mpe import simple_spread_v3
import supersuit as ss
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env
from torch.nn import ReLU
import numpy as np
import matplotlib.pyplot as plt
from pettingzoo.utils.conversions import aec_to_parallel

# Konfiguracja środowiska
env = simple_spread_v3.env(N=2, local_ratio=0.5, max_cycles=50, continuous_actions=False)
env.reset()
env = aec_to_parallel(env)
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(env, 1, num_cpus=1, base_class="stable_baselines3")

# Konfiguracja i powiększenie sieci A2C
policy_kwargs = dict(net_arch=[256, 256], activation_fn=ReLU)

model = A2C("MlpPolicy", env, verbose=1, policy_kwargs=policy_kwargs)

# Dane do wykresów
mean_rewards_agent1 = []
mean_rewards_agent2 = []
max_rewards_agent1 = []
max_rewards_agent2 = []

obs = env.reset()

for i in range(100):
    model.learn(total_timesteps=1000, reset_num_timesteps=False)
    obs = env.reset()
    episode_rewards = []

    for _ in range(25):  # Jeden "epizod" 25 kroków
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        episode_rewards.append(reward)  # reward: [nagroda_agenta1, nagroda_agenta2]

    episode_rewards = np.array(episode_rewards)

    mean_reward = episode_rewards.mean(axis=0)
    max_reward = episode_rewards.max(axis=0)

    print(f"Epizod {i+1}, średnia nagroda: {mean_reward}, maksymalna nagroda: {max_reward}")

    mean_rewards_agent1.append(mean_reward[0])
    mean_rewards_agent2.append(mean_reward[1])
    max_rewards_agent1.append(max_reward[0])
    max_rewards_agent2.append(max_reward[1])

# Zapis modelu
model.save("a2c_simple_spread")

# Wykres: średnie nagrody
plt.figure(figsize=(10, 5))
plt.plot(mean_rewards_agent1, label="Średnia nagroda - Agent 1")
plt.plot(mean_rewards_agent2, label="Średnia nagroda - Agent 2")
plt.title("A2C: Średnia nagroda na agenta")
plt.xlabel("Epizod")
plt.ylabel("Średnia nagroda")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("a2c_mean_rewards_per_agent.png")

# Wykres: maksymalne nagrody
plt.figure(figsize=(10, 5))
plt.plot(max_rewards_agent1, label="Maksymalna nagroda - Agent 1", linestyle="--")
plt.plot(max_rewards_agent2, label="Maksymalna nagroda - Agent 2", linestyle="--")
plt.title("A2C: Maksymalna nagroda na agenta")
plt.xlabel("Epizod")
plt.ylabel("Maksymalna nagroda")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("a2c_max_rewards_per_agent.png")
