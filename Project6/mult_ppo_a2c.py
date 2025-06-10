from pettingzoo.mpe import simple_spread_v3
import supersuit as ss
from stable_baselines3 import PPO, A2C
import numpy as np
import matplotlib.pyplot as plt

from pettingzoo.utils.conversions import aec_to_parallel

env = simple_spread_v3.env(N=2, local_ratio=0.5, max_cycles=25, continuous_actions=False)
env.reset()
env = aec_to_parallel(env)  # Konwersja do ParallelEnv
vec_env = ss.pettingzoo_env_to_vec_env_v1(env)
vec_env = ss.concat_vec_envs_v1(vec_env, 1, num_cpus=1, base_class="stable_baselines3")

# Load models
ppo_model = PPO.load("ppo_simple_spread")
a2c_model = A2C.load("a2c_simple_spread")

# Evaluate each configuration
def evaluate(models, label):
    rewards = []
    obs = vec_env.reset()
    for _ in range(200):
        actions = []
        for i, model in enumerate(models):
            action, _ = model.predict(obs)
            actions.append(action)
        obs, reward, done, info = vec_env.step(actions[0])  # Use joint action
        rewards.append(np.mean(reward))
    return rewards

ppo_rewards = evaluate([ppo_model, ppo_model], "PPO-PPO")
a2c_rewards = evaluate([a2c_model, a2c_model], "A2C-A2C")
mixed_rewards = evaluate([ppo_model, a2c_model], "PPO-A2C")

# Plot comparison
plt.plot(ppo_rewards, label="PPO-PPO", color='blue')
plt.plot(a2c_rewards, label="A2C-A2C", color='green')
plt.plot(mixed_rewards, label="PPO-A2C", color='orange')
plt.title("Porownanie agentow PPO, A2C i mieszanych")
plt.xlabel("Krok")
plt.ylabel("Srednia nagroda")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("comparison_learning_curves.png")