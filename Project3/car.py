import  gymnasium as gym


env = gym.make("MountainCarContinuous-v0", render_mode="rgb_array", goal_velocity=0.1)