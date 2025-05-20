from collections import defaultdict
import matplotlib.pyplot as plt
import time
import numpy as np
from collectgame import CollectEnv
import pygame
import sys
import random
import os

#for yoou to play
# if __name__ == "__main__":
#     env = CollectEnv(render_mode="human")
#     obs, _ = env.reset()
# 
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 break
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     running = False
#                     break
# 
#                 action = 4  # "none" as default
#                 if event.key == pygame.K_UP:
#                     action = 0
#                 elif event.key == pygame.K_DOWN:
#                     action = 1
#                 elif event.key == pygame.K_LEFT:
#                     action = 2
#                 elif event.key == pygame.K_RIGHT:
#                     action = 3
# 
#                 obs, reward, done, _, _ = env.step(action)
#                 env.render()
#                 print(f"Obs: {obs}, Reward: {reward}, Done: {done}")
# 
#                 if done:
#                     print("Koniec gry. Resetuję...")
#                     obs, _ = env.reset()
# 
#     env.close()
#     pygame.quit()
#     sys.exit()

# env = CollectEnv()
class Agent:
    def __init__(self, env, alpha=0.2, gamma=0.8, epsilon=0.2, epsilon_decay=0.005, min_epsilon=0.01):
        self.env = env
        self.q_table = defaultdict(lambda: np.zeros(env.action_space.n))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def get_state(self, obs):
        return tuple(obs['position'])

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.q_table[state])

    def train_q_learning(self, episodes=1000):
        rewards = []
        times = []

        for episode in range(episodes):
            start_time = time.time()

            obs, _ = self.env.reset()
            state = self.get_state(obs)
            total_reward = 0
            done = False

            while not done:
                action = self.choose_action(state)
                next_obs, reward, done, _, _ = self.env.step(action)
                next_state = self.get_state(next_obs)

                best_next = np.max(self.q_table[next_state])
                self.q_table[state][action] += self.alpha * (reward + self.gamma * best_next - self.q_table[state][action])

                state = next_state
                total_reward += reward

            end_time = time.time()
            duration = end_time - start_time

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            rewards.append(total_reward)
            times.append(duration)

            if episode % 100 == 0:
                print(f"[Q] Episode {episode} | Reward: {total_reward:.1f} | Time: {duration:.4f} sec")

        self.plot_results(rewards, times, "Q-learning")
        return rewards, times

    def train_sarsa(self, episodes=1000):
        rewards = []
        times = []

        for episode in range(episodes):
            start_time = time.time()

            obs, _ = self.env.reset()
            state = self.get_state(obs)
            action = self.choose_action(state)
            total_reward = 0
            done = False

            while not done:
                next_obs, reward, done, _, _ = self.env.step(action)
                next_state = self.get_state(next_obs)
                next_action = self.choose_action(next_state)

                self.q_table[state][action] += self.alpha * (
                        reward + self.gamma * self.q_table[next_state][next_action] - self.q_table[state][action]
                )

                state, action = next_state, next_action
                total_reward += reward

            end_time = time.time()
            duration = end_time - start_time

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            rewards.append(total_reward)
            times.append(duration)

            if episode % 100 == 0:
                print(f"[SARSA] Episode {episode} | Reward: {total_reward:.1f} | Time: {duration:.4f} sec")

        self.plot_results(rewards, times, "SARSA")
        return rewards, times

    def plot_results(self, rewards, times, title):
        episodes = range(len(rewards))

        plt.figure(figsize=(12, 5))

        # Wykres punktów
        plt.subplot(1, 2, 1)
        plt.plot(episodes, rewards, label="Punkty")
        plt.xlabel("Epizod")
        plt.ylabel("Suma nagród")
        plt.title(f"{title} – Nagrody")

        # Wykres czasu
        plt.subplot(1, 2, 2)
        plt.plot(episodes, times, label="Czas", color='orange')
        plt.xlabel("Epizod")
        plt.ylabel("Czas trwania (s)")
        plt.title(f"{title} – Czas epizodu")

        plt.tight_layout()

        # Zapis wykresu
        folder = "wykresy"
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/{title.replace(' ', '_').lower()}_plot.png"
        plt.savefig(filename)
        plt.close()


env = CollectEnv()
agent = Agent(env)

# Q-learning
#rewards, times = agent.train_q_learning(episodes=10000)

# SARSA
rewards, times = agent.train_sarsa(episodes=5000)