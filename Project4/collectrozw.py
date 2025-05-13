import numpy as np
from collectgame import CollectEnv

env = CollectEnv()

# Parametry Q-learningu
alpha = 0.1       # tempo uczenia
gamma = 0.9      # współczynnik dyskontowy
epsilon = 0.3     # eksploracja
episodes = 2000   # liczba epizodów treningowych

# Inicjalizacja Q-tabeli
q_table = np.zeros((20, 20, env.max_steps + 1, env.action_space.n))

def get_action(state):
    if np.random.rand() < epsilon:
        return env.action_space.sample()
    x, y, step = state
    return np.argmax(q_table[x, y, step])

def discretize(obs):
    x, y = obs["position"]
    step = obs["step"]
    return x, y, step

for ep in range(episodes):
    obs, _ = env.reset()
    total_reward = 0

    for _ in range(env.max_steps):
        x, y, step = discretize(obs)
        action = get_action((x, y, step))
        next_obs, reward, done, _, _ = env.step(action)
        nx, ny, nstep = discretize(next_obs)

        # Aktualizacja Q
        best_next_q = np.max(q_table[nx, ny, nstep])
        q_table[x, y, step, action] += alpha * (reward + gamma * best_next_q - q_table[x, y, step, action])
        obs = next_obs
        total_reward += reward

        if done:
            break

    if (ep + 1) % 10 == 0:
        print(f"Episode {ep+1}, Total reward: {total_reward:.2f}")

print("Trening zakończony!")
