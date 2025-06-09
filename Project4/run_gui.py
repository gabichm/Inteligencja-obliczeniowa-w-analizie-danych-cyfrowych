from collectgame import CollectEnv 
import pygame
import numpy as np


print("Starting game...")

env = CollectEnv(render_mode="human")
# obs, _ = env.reset()
print("Initial observation:", env.agent_pos)


done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    env.render()

env.close()