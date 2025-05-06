import gymnasium as gym
from gymnasium.spaces import Discrete
import numpy as np
import matplotlib.pyplot as plt
from typing import cast
from collections import defaultdict
import time
import csv

env = gym.make('CliffWalking-v0')
action_space = cast(Discrete, env.action_space)
observation_space = cast(Discrete, env.observation_space)


def epsilon_greedy(Q, state, n_actions, epsilon):
    if np.random.rand() < epsilon:
        return np.random.choice(n_actions)
    return np.argmax(Q[state])


def q_learning(env, episodes, alpha, gamma, epsilon):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    episode_rewards = []
    episode_steps = []

    for ep in range(episodes):
        state, _ = env.reset()
        total_reward = 0
        steps = 0
        done = False

        while not done:
            action = epsilon_greedy(Q, state, env.action_space.n, epsilon)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            total_reward += reward
            steps += 1

            best_next_action = np.argmax(Q[next_state])
            td_target = reward + gamma * Q[next_state][best_next_action]
            Q[state][action] += alpha * (td_target - Q[state][action])
            state = next_state

        episode_rewards.append(total_reward)
        episode_steps.append(steps)

    return Q, episode_rewards, episode_steps


def sarsa(env, episodes, alpha, gamma, epsilon):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    episode_rewards = []
    episode_steps = []

    for ep in range(episodes):
        state, _ = env.reset()
        action = epsilon_greedy(Q, state, env.action_space.n, epsilon)
        total_reward = 0
        steps = 0
        done = False

        while not done:
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            next_action = epsilon_greedy(Q, next_state, env.action_space.n, epsilon)
            total_reward += reward
            steps += 1

            td_target = reward + gamma * Q[next_state][next_action]
            Q[state][action] += alpha * (td_target - Q[state][action])
            state, action = next_state, next_action

        episode_rewards.append(total_reward)
        episode_steps.append(steps)

    return Q, episode_rewards, episode_steps


# Parametry
gammas = [0.9, 0.7]  # wspolczynnik dyskontowy
alphas = [0.1, 0.3, 0.5]  # wspolczynnik uczenia
epsilons = [0.1, 0.3, 0.5]  # wspolczynnik eksploracji
episodes = 500

with open('wyniki_hiperparametry.csv', 'w', newline='') as csvfile:
    fieldnames = ['algorytm', 'alpha', 'gamma', 'epsilon', 'suma_nagrod', 'srednia_nagroda', 'najlepszy_wynik', 'srednia_kroki', 'czas']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for alpha in alphas:
        for epsilon in epsilons:
            for gamma in gammas:
                # Q-Learning
                start = time.time()
                _, rewards_q, steps_q = q_learning(env, 1000, alpha, gamma, epsilon)
                end = time.time()
                writer.writerow({
                    'algorytm': 'Q-Learning',
                    'alpha': alpha,
                    'gamma': gamma,
                    'epsilon': epsilon,
                    'suma_nagrod': np.sum(rewards_q),
                    'srednia_nagroda': np.mean(rewards_q),
                    'najlepszy_wynik': np.max(rewards_q),
                    'srednia_kroki': np.mean(steps_q),
                    'czas': round(end - start, 3)
                })

                # SARSA
                start = time.time()
                _, rewards_s, steps_s = sarsa(env, 1000, alpha, gamma, epsilon)
                end = time.time()
                writer.writerow({
                    'algorytm': 'SARSA',
                    'alpha': alpha,
                    'gamma': gamma,
                    'epsilon': epsilon,
                    'suma_nagrod': np.sum(rewards_s),
                    'srednia_nagroda': np.mean(rewards_s),
                    'najlepszy_wynik': np.max(rewards_s),
                    'srednia_kroki': np.mean(steps_s),
                    'czas': round(end - start, 3)
                })
# # Q-learning
# q_start_t = time.time()
# q_Q, q_rewards, q_steps = q_learning(env, episodes, alpha, gamma, epsilon)
# end_q_t = time.time()
# q_t = end_q_t - q_start_t
# 
# # Sarsa
# s_start_t = time.time()
# sarsa_Q, sarsa_rewards, sarsa_steps = sarsa(env, episodes, alpha, gamma, epsilon)
# end_s_t = time.time()
# s_t = end_s_t - s_start_t
# 
# # --- WYKRESY ---
# 
# # Wykres punktów zdobytych w epizodach
# plt.figure(figsize=(12, 6))
# plt.plot(q_rewards, label="Q-Learning", color='purple', alpha=0.6)
# plt.plot(sarsa_rewards, label="SARSA", color='green', alpha=0.6)
# plt.xlabel("Epizod")
# plt.ylabel("Liczba punktów zdobytych")
# plt.title("Porównanie Q-Learning i SARSA - Cliff Walking")
# plt.legend()
# plt.grid(True)
# plt.savefig("reward_q_vs_s.png")
# plt.close()
# # Wykres liczby kroków
# plt.figure(figsize=(12, 6))
# plt.plot(q_steps, label="Q-Learning", color='blue', alpha=0.6)
# plt.plot(sarsa_steps, label="SARSA", color='green', alpha=0.6)
# plt.xlabel("Epizod")
# plt.ylabel("Liczba kroków")
# plt.title("Liczba kroków w epizodzie - Q-Learning vs SARSA")
# plt.legend()
# plt.grid(True)
# plt.savefig("steps_q_vs_s.png")
# 
# 
# # ---POROWNANIE WYNIKOW---
# 
# # Najlepsze wynik
# best_q_reward_ep = np.argmax(q_rewards)
# best_sarsa_reward_ep = np.argmax(sarsa_rewards)
# 
# # Kroki do celu
# best_q_step_ep = np.argmin(q_steps)
# best_sarsa_step_ep = np.argmin(sarsa_steps)
# 
# print("Q-Learning:")
# print(f"  Najwyższa liczba punktów: {q_rewards[best_q_reward_ep]} w epizodzie {best_q_reward_ep}")
# print(f"  Najmniej kroków: {q_steps[best_q_step_ep]} w epizodzie {best_q_step_ep}")
# print(f"Czas wykonania : {q_t:.3f} sekund")
# 
# print("SARSA:")
# print(f"  Najwyższa liczba punktów: {sarsa_rewards[best_sarsa_reward_ep]} w epizodzie {best_sarsa_reward_ep}")
# print(f"  Najmniej kroków: {sarsa_steps[best_sarsa_step_ep]} w epizodzie {best_sarsa_step_ep}")
# print(f"Czas wykonania : {s_t:.3f} sekund")
