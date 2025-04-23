import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

env = gym.make('CliffWalking-v0')

#parametry
disc = 0.9 #współczynnik dyskontowy
learning_rate = 0.1 #wspołczynik uczenia
epsilon = 0.1 #wspolczynnik eksploracji

episodes = 200
max_steps = 100 

act_space  = env.action_space
obs_space = env.observation_space
Q = np.zeros((act_space, obs_space))

points =[]

for e in range(episodes):
    state, _ = env.reset()
    total_points = 0
    done = False

    for max_steps in range(max_steps):
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state,:])
