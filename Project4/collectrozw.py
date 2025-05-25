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
if __name__ == "__main__":
    env = CollectEnv(render_mode="human")
    obs, _ = env.reset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

                action = 4  # "none" as default
                if event.key == pygame.K_UP:
                    action = 0
                elif event.key == pygame.K_DOWN:
                    action = 1
                elif event.key == pygame.K_LEFT:
                    action = 2
                elif event.key == pygame.K_RIGHT:
                    action = 3

                obs, reward, done, _, _ = env.step(action)
                env.render()
                print(f"Obs: {obs}, Reward: {reward}, Done: {done}")

                if done:
                    print("Koniec gry. Resetuję...")
                    obs, _ = env.reset()

    env.close()
    pygame.quit()
    sys.exit()

def extract_state(obs):
    dx = np.clip(obs["target_delta"][0], -10, 10)
    dy = np.clip(obs["target_delta"][1], -10, 10)
    return (
        obs["position"][0],
        obs["position"][1],
        dx,
        dy,
        obs["target_type"]
    )


def epsilon_greedy_policy(Q, state, epsilon, n_actions):
    if np.random.rand() < epsilon:
        return np.random.randint(n_actions)
    return np.argmax(Q[state])


def train_q_learning(env, episodes=500, alpha=0.1, gamma=0.9, epsilon=0.1):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    episode_rewards = []
    episode_times = []

    for ep in range(episodes):
        obs, _ = env.reset()
        state = extract_state(obs)

        total_reward = 0
        start_time = time.time()

        done = False
        while not done:
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state])

            next_obs, reward, done, _, _ = env.step(action)
            next_state = extract_state(next_obs)

            best_next_action = np.argmax(Q[next_state])
            td_target = reward + gamma * Q[next_state][best_next_action]
            Q[state][action] += alpha * (td_target - Q[state][action])

            state = next_state
            total_reward += reward

        episode_rewards.append(total_reward)
        episode_times.append(time.time() - start_time)
        if (ep + 1) % 100 == 0:
            print(f"Q-Learning - Episode {ep + 1}, reward: {total_reward:.2f}")

    return Q, episode_rewards, episode_times


def train_sarsa(env, episodes=500, alpha=0.1, gamma=0.9, epsilon=0.1):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    episode_rewards = []
    episode_times = []

    for ep in range(episodes):
        obs, _ = env.reset()
        state = extract_state(obs)

        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])

        total_reward = 0
        start_time = time.time()

        done = False
        while not done:
            next_obs, reward, done, _, _ = env.step(action)
            next_state = extract_state(next_obs)

            if random.random() < epsilon:
                next_action = env.action_space.sample()
            else:
                next_action = np.argmax(Q[next_state])

            td_target = reward + gamma * Q[next_state][next_action]
            Q[state][action] += alpha * (td_target - Q[state][action])

            state = next_state
            action = next_action
            total_reward += reward

        episode_rewards.append(total_reward)
        episode_times.append(time.time() - start_time)

        if (ep + 1) % 100 == 0:
            print(f"Sarsa-Learning - Episode {ep + 1}, reward: {total_reward:.2f}")

    return Q, episode_rewards, episode_times


def plot_training(rewards, times, method_name, save_dir="wykresy"):
    os.makedirs(save_dir, exist_ok=True)
    episodes = list(range(1, len(rewards) + 1))

    plt.figure(figsize=(14, 5))

    # Reward vs Episode
    plt.subplot(1, 2, 1)
    plt.plot(episodes, rewards, label="Reward", color="blue")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title(f"{method_name}: Reward vs Episode")
    plt.grid(True)

    # Time vs Episode
    plt.subplot(1, 2, 2)
    plt.plot(episodes, times, label="Time", color="green")
    plt.xlabel("Episode")
    plt.ylabel("Time (seconds)")
    plt.title(f"{method_name}: Time vs Episode")
    plt.grid(True)

    plt.tight_layout()

    # Zapis do pliku
    filename = f"{method_name.lower().replace(' ', '_')}_training_plot.png"
    plt.savefig(os.path.join(save_dir, filename))
    plt.close()


env = CollectEnv(render_mode=None)

q_table, q_rewards, q_times = train_q_learning(env, episodes=5000)
plot_training(q_rewards, q_times, method_name="Q-Learning")

# sarsa_table, sarsa_rewards, sarsa_times = train_sarsa(env, episodes=5000)
# plot_training(sarsa_rewards, sarsa_times, method_name="SARSA")

