import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize
from stable_baselines3.common.callbacks import BaseCallback

import numpy as np
import time
import matplotlib.pyplot as plt
import csv

class EpisodeLogger(BaseCallback):
    def __init__(self, max_episodes, verbose=0):
        super().__init__(verbose)
        self.max_episodes = max_episodes  # Liczba epizodów, po której zakończymy trening
        self.episode_rewards = []
        self.episode_max_positions = []
        self.episode_steps_to_goal = []
        self.episode_count = 0  # Licznik epizodów

    def _on_step(self) -> bool:
        infos = self.locals["infos"]
        dones = self.locals["dones"]
        obs = self.locals["new_obs"]

        for i, done in enumerate(dones):
            if done:
                # Zliczanie epizodow
                self.episode_count += 1

                # reward z epizodu
                reward = self.locals["rewards"][i]
                self.episode_rewards.append(reward)

                # pozycja samochodu 
                max_pos = max(float(obs[i][0]), self.episode_max_positions[-1] if self.episode_max_positions else -np.inf)

                self.episode_max_positions.append(max_pos)

               
                if max_pos >= 0.45:
                    steps_to_goal = self.locals["n_steps"]
                    self.episode_steps_to_goal.append(steps_to_goal)
                else:
                    self.episode_steps_to_goal.append(-1)

                print(f"🏁 Epizod zakończony | Reward: {reward:.2f} | Max pozycja: {max_pos:.4f}")

        # Zatrzymanie treningu po osiągnięciu max_episodes
        if self.episode_count >= self.max_episodes:
            print(f"🏁 Zakończono trening po {self.max_episodes} epizodach!")
            return False  # Zakończ trening

        return True


env = make_vec_env("MountainCarContinuous-v0", n_envs=1)
env = VecNormalize(env, norm_obs=True, norm_reward=False)

# Hiperparametry PPO
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=3e-4,
    gamma=0.9765, 
    gae_lambda=0.9766,
    n_steps=2048,
    batch_size=64,
    ent_coef=0.1,  
    n_epochs=10,
    clip_range=0.2,
    tensorboard_log="./ppo_log"
)

# Liczba epizodów maksymalna
max_episodes = 100  

# Trening
start = time.time()
callback = EpisodeLogger(max_episodes=max_episodes)  # Dodajemy licznik epizodów
model.learn(total_timesteps=1_000_000, callback=callback)
end = time.time()
print(f"⏱ Trening trwał {(end - start):.2f} sekundy")


model.save("ppo_mountaincar")
env.save("vec_normalize.pkl")
print("📦 Model i normalizacja zapisane")


# normalizacja  w testowym środowisku
test_env = gym.make("MountainCarContinuous-v0", render_mode="human")
test_env = make_vec_env(lambda: test_env, n_envs=1)
test_env = VecNormalize.load("vec_normalize.pkl", test_env)
test_env.training = False  
obs = test_env.reset()
done = False
episode_reward = 0
max_position = float(obs[0][0])  

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated = test_env.step(action)
    done = terminated or truncated
    episode_reward += float(reward)
    max_position = max(max_position, float(obs[0][0]))

    test_env.render()

episode_reward = float(episode_reward)  
print(f"Reward z testu: {episode_reward:.2f}")
print(f"Największa osiągnięta pozycja: {max_position:.4f}")


episodes = np.arange(len(callback.episode_rewards))


# Wykres 1: Nagroda
plt.figure(figsize=(6, 4))
plt.plot(episodes, callback.episode_rewards, label="Nagroda")
plt.xlabel("Epizod")
plt.ylabel("Nagroda")
plt.title("Nagroda w każdym epizodzie")
plt.grid(True)
plt.tight_layout()
plt.savefig('reward_per_episode.png')
plt.close()  

# Wykres 2: Maksymalna pozycja
plt.figure(figsize=(6, 4))
plt.plot(episodes, callback.episode_max_positions, label="Max Pozycja", color="orange")
plt.xlabel("Epizod")
plt.ylabel("Maksymalna pozycja")
plt.title("Maksymalna pozycja w każdym epizodzie")
plt.grid(True)
plt.tight_layout()
plt.savefig('max_position_per_episode.png')
plt.close()



# Zapis wyników do pliku CSV
with open('episode_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Epizod", "Nagroda", "Maksymalna Pozycja", "Kroki do Celu"])
    for i in range(len(callback.episode_rewards)):
        writer.writerow([i, callback.episode_rewards[i], callback.episode_max_positions[i], callback.episode_steps_to_goal[i]])

test_env.close()
