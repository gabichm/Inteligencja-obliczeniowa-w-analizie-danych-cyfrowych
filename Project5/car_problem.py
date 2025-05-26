import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import VecNormalize
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import time
import matplotlib.pyplot as plt
import csv
from stable_baselines3.common.vec_env import DummyVecEnv


# --- Ustawienia ---
env_id = "MountainCarContinuous-v0"
total_timesteps = 50000
num_runs = 10  # liczba powtórzeń dla każdego zestawu hiperparametrów
log_interval = 1000  # co ile kroków zbieramy nagrodę

# Zestawy hiperparametrów do testu
hyperparams = {
    "A": {"learning_rate": 3e-4, "clip_range": 0.2, "gamma": 0.99, "gae_lambda": 0.95},
    "B": {"learning_rate": 1e-4, "clip_range": 0.1, "gamma": 0.95, "gae_lambda": 0.9},
    "C": {"learning_rate": 5e-4, "clip_range": 0.3, "gamma": 0.99, "gae_lambda": 0.95},
}

def make_env(seed):
    def _init():
        env = gym.make(env_id)
        env.seed(seed)
        env.action_space.seed(seed)
        return env
    return _init

def train_and_collect(params, seed):
    env = DummyVecEnv([make_env(seed)])
    model = PPO("MlpPolicy", env, verbose=0,
                learning_rate=params["learning_rate"],
                clip_range=params["clip_range"],
                gamma=params["gamma"],
                gae_lambda=params["gae_lambda"],
                seed=seed)

    rewards = []
    obs = env.reset()
    episode_rewards = 0
    episode_step = 0
    collected_rewards = []

    start_time = time.time()
    for step in range(1, total_timesteps + 1):
        action, _states = model.predict(obs, deterministic=False)
        obs, reward, done, info = env.step(action)
        episode_rewards += reward[0]
        episode_step += 1

        model.rollout_buffer.add(obs, action, reward, done, _states)  # internal buffer update

        if done:
            obs = env.reset()
            collected_rewards.append(episode_rewards)
            episode_rewards = 0
            episode_step = 0

        # co log_interval kroków zapisz średnią nagrodę z epizodu lub 0 jeśli brak
        if step % log_interval == 0:
            if collected_rewards:
                avg_r = np.mean(collected_rewards[-10:])
            else:
                avg_r = 0
            rewards.append(avg_r)

        model.train()  # aktualizacja modelu co krok

    end_time = time.time()
    env.close()

    return rewards, end_time - start_time

def main():
    results = {}

    for name, params in hyperparams.items():
        print(f"Start training set {name}...")
        all_runs_rewards = []
        times = []
        for run in range(num_runs):
            seed = 1000 + run
            rewards, elapsed = train_and_collect(params, seed)
            all_runs_rewards.append(rewards)
            times.append(elapsed)
            print(f"Run {run+1}/{num_runs} done, time: {elapsed:.1f}s")

        all_runs_rewards = np.array(all_runs_rewards)  # shape (num_runs, steps)
        mean_rewards = np.mean(all_runs_rewards, axis=0)
        std_rewards = np.std(all_runs_rewards, axis=0)
        avg_time = np.mean(times)

        results[name] = {
            "mean": mean_rewards,
            "std": std_rewards,
            "time": avg_time
        }

    # Rysowanie wykresów
    steps = np.arange(log_interval, total_timesteps + 1, log_interval)

    plt.figure(figsize=(12, 8))
    for name in hyperparams.keys():
        plt.plot(steps, results[name]["mean"], label=f"Set {name}")
        plt.fill_between(steps,
                         results[name]["mean"] - results[name]["std"],
                         results[name]["mean"] + results[name]["std"],
                         alpha=0.2)
    plt.title("Średnia nagroda w zależności od kroku czasowego")
    plt.xlabel("Krok czasowy")
    plt.ylabel("Średnia nagroda")
    plt.legend()
    plt.grid()
    plt.show()

    for name in hyperparams.keys():
        print(f"Set {name} avg time for {total_timesteps} steps: {results[name]['time']:.2f}s")

if __name__ == "__main__":
    main()
