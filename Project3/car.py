import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import matplotlib.pyplot as plt

# Ustawienia
ENV_NAME = "MountainCarContinuous-v0"
SEED = 123
MAX_EPISODES = 300
MAX_STEPS = 999
BATCH_SIZE = 64
GAMMA = 0.99
TAU = 0.005
ACTOR_LR = 1e-4
CRITIC_LR = 1e-3
MEMORY_CAPACITY = 1000000

# Reproducibility
torch.manual_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)

# Actor network
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim, max_action):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 400),
            nn.ReLU(),
            nn.Linear(400, 300),
            nn.ReLU(),
            nn.Linear(300, action_dim),
            nn.Tanh()
        )
        self.max_action = max_action

    def forward(self, state):
        return self.max_action * self.fc(state)

# Critic network
class Critic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim + action_dim, 400),
            nn.ReLU(),
            nn.Linear(400, 300),
            nn.ReLU(),
            nn.Linear(300, 1)
        )

    def forward(self, state, action):
        x = torch.cat([state, action], 1)
        return self.fc(x)

# Replay buffer
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, transition):
        self.buffer.append(transition)

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
        return (
            torch.FloatTensor(states),
            torch.FloatTensor(actions),
            torch.FloatTensor(rewards).unsqueeze(1),
            torch.FloatTensor(next_states),
            torch.FloatTensor(dones).unsqueeze(1)
        )

    def __len__(self):
        return len(self.buffer)

# Agent DDPG
class DDPGAgent:
    def __init__(self, state_dim, action_dim, max_action):
        self.actor = Actor(state_dim, action_dim, max_action)
        self.actor_target = Actor(state_dim, action_dim, max_action)
        self.actor_target.load_state_dict(self.actor.state_dict())

        self.critic = Critic(state_dim, action_dim)
        self.critic_target = Critic(state_dim, action_dim)
        self.critic_target.load_state_dict(self.critic.state_dict())

        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=ACTOR_LR)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=CRITIC_LR)

        self.replay_buffer = ReplayBuffer(MEMORY_CAPACITY)
        self.max_action = max_action

    def select_action(self, state, noise=0.1):
        state = torch.FloatTensor(state.reshape(1, -1))
        action = self.actor(state).detach().cpu().numpy()[0]
        return (action + noise * np.random.randn(*action.shape)).clip(-self.max_action, self.max_action)

    def train(self):
        if len(self.replay_buffer) < BATCH_SIZE:
            return

        state, action, reward, next_state, done = self.replay_buffer.sample(BATCH_SIZE)

        # Critic loss
        with torch.no_grad():
            target_action = self.actor_target(next_state)
            target_q = self.critic_target(next_state, target_action)
            y = reward + GAMMA * (1 - done) * target_q

        critic_loss = nn.MSELoss()(self.critic(state, action), y)

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Actor loss
        actor_loss = -self.critic(state, self.actor(state)).mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # Soft update
        for param, target_param in zip(self.critic.parameters(), self.critic_target.parameters()):
            target_param.data.copy_(TAU * param.data + (1 - TAU) * target_param.data)
        for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
            target_param.data.copy_(TAU * param.data + (1 - TAU) * target_param.data)

# Trening
env = gym.make(ENV_NAME)
env.reset(seed=SEED)
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.shape[0]
max_action = float(env.action_space.high[0])
agent = DDPGAgent(state_dim, action_dim, max_action)

episode_rewards = []

for episode in range(MAX_EPISODES):
    state, _ = env.reset()
    episode_reward = 0

    for step in range(MAX_STEPS):
        action = agent.select_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        agent.replay_buffer.add((state, action, reward, next_state, float(done)))
        state = next_state
        episode_reward += reward

        agent.train()

        if done:
            break

    episode_rewards.append(episode_reward)
    print(f"Episode {episode + 1}: reward = {episode_reward:.2f}")

# Wykres
plt.plot(episode_rewards)
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("DDPG on MountainCarContinuous-v0")
plt.show()



# import gymnasium as gym
# from stable_baselines3 import PPO
# from stable_baselines3.common.env_util import make_vec_env
# from stable_baselines3.common.vec_env import VecNormalize
# import numpy as np
# import time

# # Utwórz środowisko treningowe z normalizacją obserwacji
# env = make_vec_env(lambda: gym.make("MountainCarContinuous-v0", goal_velocity=0.1), n_envs=1)
# env = VecNormalize(env, norm_obs=True, norm_reward=False)

# # ⚙️ Lepsze hiperparametry dla MountainCarContinuous
# model = PPO(
#     "MlpPolicy",
#     env,
#     verbose=1,
#     learning_rate=3e-4,
#     gamma=0.98,
#     gae_lambda=0.9,
#     n_steps=2048,
#     batch_size=64,
#     ent_coef=0.0,
#     n_epochs=10,
#     clip_range=0.2,
#     tensorboard_log="./ppo_log"
# )

# # ⏱ Trening + pomiar FPS
# start_time = time.time()
# model.learn(total_timesteps=1_000_000)
# end_time = time.time()
# print(f"⏱ Trening trwał {(end_time - start_time):.2f} sekundy")

# # 💾 Zapisz model + normalizację
# model.save("ppo_mountaincar")
# env.save("vec_normalize.pkl")
# print("📦 Model i normalizacja zapisane")

# # 🧪 Testowanie z tą samą normalizacją
# test_env = gym.make("MountainCarContinuous-v0", render_mode="human", goal_velocity=0.1)
# test_env = VecNormalize.load("vec_normalize.pkl", test_env)
# test_env.training = False  # wyłącz aktualizację statystyk normalizacji

# obs, _ = test_env.reset()
# done = False
# episode_reward = 0

# while not done:
#     action, _ = model.predict(obs, deterministic=True)
#     obs, reward, terminated, truncated, _ = test_env.step(action)
#     done = terminated or truncated
#     episode_reward += reward
#     test_env.render()

# test_env.close()

# # 📊 Zapisz wynik
# with open("ppo_rewards.txt", "w") as f:
#     f.write(f"{episode_reward}\n")
# print(f"📈 Nagroda z testu: {episode_reward:.2f}")
