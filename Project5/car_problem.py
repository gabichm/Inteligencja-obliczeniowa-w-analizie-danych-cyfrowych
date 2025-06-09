import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.evaluation import evaluate_policy
import numpy as np
import matplotlib.pyplot as plt
import time

# --- Ustawienia ---
env_id = "MountainCarContinuous-v0"
total_timesteps = 50000
num_runs = 10
eval_interval = 5000  # co ile kroków oceniamy
n_eval_episodes = 10

# Zestawy hiperparametrów
hyperparams = {
    "A": {"learning_rate": 1e-5, "clip_range": 0.2, "gamma": 0.99, "gae_lambda": 0.95, "n_steps": 512},
    "B": {"learning_rate": 1e-4, "clip_range": 0.2, "gamma": 0.99, "gae_lambda": 0.95, "n_steps": 1024},
    "C": {"learning_rate": 1e-3, "clip_range": 0.3, "gamma": 0.99, "gae_lambda": 0.95, "n_steps": 2048},
}

def make_env(seed):
    def _init():
        env = gym.make(env_id)
        env.reset(seed=seed)
        env.action_space.seed(seed)
        return env
    return _init

def train_and_evaluate(params, seed):
    env = DummyVecEnv([make_env(seed)])
    env = VecNormalize(env, norm_reward = True)
    model = PPO("MlpPolicy", env, verbose=0,
                learning_rate=params["learning_rate"],
                clip_range=params["clip_range"],
                gamma=params["gamma"],
                gae_lambda=params["gae_lambda"],
                n_steps=params['n_steps'],
                seed=seed)

    rewards = []
    timesteps_so_far = 0

    while timesteps_so_far < total_timesteps:
        model.learn(total_timesteps=eval_interval, reset_num_timesteps=False)
        timesteps_so_far += eval_interval

        mean_reward, _ = evaluate_policy(model, env, n_eval_episodes, deterministic=True, return_episode_rewards=False)
        rewards.append(mean_reward)
    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _ = env.step(action)
        env.render()


    env.close()
    return rewards

def main():
    results = {}
    steps = np.arange(eval_interval, total_timesteps + 1, eval_interval)

    for name, params in hyperparams.items():
        print(f"Trening zestawu {name}...")
        all_runs_rewards = []
        for run in range(num_runs):
            seed = 1000 + run
            rewards = train_and_evaluate(params, seed)
            all_runs_rewards.append(rewards)
            print(f"Run {run+1}/{num_runs} done")

        all_runs_rewards = np.array(all_runs_rewards)
        mean_rewards = np.mean(all_runs_rewards, axis=0)
        std_rewards = np.std(all_runs_rewards, axis=0)

        results[name] = {"mean": mean_rewards, "std": std_rewards}
        

    # Rysowanie wykresów
    plt.figure(figsize=(12, 8))
    for name in hyperparams:
        plt.plot(steps, results[name]["mean"], label=f"Zestaw {name}")
        plt.fill_between(steps,
                         results[name]["mean"] - results[name]["std"],
                         results[name]["mean"] + results[name]["std"],
                         alpha=0.2)
    plt.title("Średnia nagroda vs. liczba kroków czasowych")
    plt.xlabel("Kroki czasowe")
    plt.ylabel("Średnia nagroda (z 5 epizodów)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
