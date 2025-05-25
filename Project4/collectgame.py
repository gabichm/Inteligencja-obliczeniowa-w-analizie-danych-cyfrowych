import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import List, Tuple, Optional, Dict
import pygame
import os
import sys
import random


class CollectEnv(gym.Env):

    metadata = {"render_modes": ["human", "ansi"]}

    ACTIONS = ["up", "down", "left", "right", "none"]
    ACTION_MAP = {
        0: (-1, 0),   # up
        1: (1, 0),    # down
        2: (0, -1),   # left
        3: (0, 1),    # right
        4: (0, 0),    # none
    }

    def __init__(self, render_mode: Optional[str] = None):
        super().__init__()
        self.grid_size = (20, 20)
        self.cell_size = 20
        self.window_size = (self.grid_size[1] * self.cell_size, self.grid_size[0] * self.cell_size + 40)
        self.max_steps = 125
        self.start_pos = (10, 10)
        self.render_mode = render_mode

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Dict({
            "position": spaces.Box(low=0, high=19, shape=(2,), dtype=np.int32),
            "step": spaces.Discrete(self.max_steps + 1),
        })
        self.assets = {}
        if render_mode == "human":
            pygame.init()
            self.window = pygame.display.set_mode(self.window_size)
            self.clock = pygame.time.Clock()
            self.load_assets()

        self.spawn_schedule: List[Tuple[int, str, Tuple[int, int]]] = [
            (0, "fruit", (2, 17)), (4, "candy", (3, 14)), (7, "fruit", (6, 6)),
            (17, "fruit", (10, 10)), (23, "candy", (15, 2)), (24, "fruit", (1, 1)),
            (27, "fruit", (11, 8)), (33, "fruit", (19, 19)), (36, "candy", (6, 0)),
            (37, "fruit", (2, 2)), (40, "candy", (3, 4)), (33, "fruit", (10, 6)),
            (45, "fruit", (14, 10)), (54, "fruit", (15, 2)), (59, "fruit", (19, 11)),
            (60, "candy", (8, 8)), (63, "candy", (7, 13)), (66, "fruit", (1, 6)),
            (75, "fruit", (4, 13)), (79, "candy", (9, 19)), (82, "fruit", (8, 15)),
            (83, "fruit", (10, 10)), (84, "candy", (17, 12)), (89, "fruit", (14, 11)),
            (94, "fruit", (8, 8)), (98, "fruit", (5, 13)), (99, "candy", (7, 14)),
            (105, "fruit", (10, 16)), (111, "candy", (8, 19)), (115, "fruit", (7, 19)),
        ]
        self.window = None
        self.clock = None
        self.reset()

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.agent_pos = list(self.start_pos)
        self.current_step = 0
        self.score = 0
        self.objects: Dict[Tuple[int, int], Tuple[str, int]] = {}
        self.game_over = False
        self.game_over_time = None
        return self._get_obs(), {}

    def step(self, action: int):
        assert self.action_space.contains(action), f"Invalid action: {action}"

    # Spawn new objects
        for spawn_time, obj_type, pos in self.spawn_schedule:
            if spawn_time == self.current_step:
                self.objects[pos] = (obj_type, self.current_step)  
    
        # Remove expired objects (after 30 steps)
        expired_positions = [
            pos for pos, (_, spawn_step) in self.objects.items()
            if self.current_step - spawn_step >= 30
        ]
        for pos in expired_positions:
            del self.objects[pos]
    
        # Move agent
        delta = self.ACTION_MAP[action]
        new_row = min(max(self.agent_pos[0] + delta[0], 0), self.grid_size[0] - 1)
        new_col = min(max(self.agent_pos[1] + delta[1], 0), self.grid_size[1] - 1)
        self.agent_pos = [new_row, new_col]
    
        # Check for item pickup
        reward = 0
        pos_tuple = tuple(self.agent_pos)
        if pos_tuple in self.objects:
            obj_type, _ = self.objects[pos_tuple]
            if obj_type == "fruit":
                reward += 10
            elif obj_type == "candy":
                reward -= 10
            del self.objects[pos_tuple]
    
        # Action penalty
        if action in [0, 1, 2, 3]:  # up/down/left/right
            reward -= 0.05
    
        self.score += reward
        self.current_step += 1
        terminated = self.current_step >= self.max_steps
        self.game_over = terminated
    
        return self._get_obs(), reward, terminated, False, {}

    def _get_obs(self):
        pos = np.array(self.agent_pos, dtype=np.int32)

        # Znajdź najbliższy cel
        min_dist = float("inf")
        target_delta = (0, 0)
        target_type = 0  # 0 = brak, 1 = fruit, -1 = candy
    
        for (obj_x, obj_y), (obj_type, _) in self.objects.items():
            dx = obj_x - self.agent_pos[0]
            dy = obj_y - self.agent_pos[1]
            dist = abs(dx) + abs(dy)
            if dist < min_dist:
                min_dist = dist
                target_delta = (dx, dy)
                target_type = 1 if obj_type == "fruit" else -1
    
        return {
            "position": pos,
            "step": self.current_step,
            "target_delta": np.array(target_delta, dtype=np.int32),
            "target_type": target_type,
        }

    def load_assets(self):
        self.assets["agent"] = pygame.image.load(os.path.join("pictures", "girl.png"))
        self.assets["fruit"] = pygame.image.load(os.path.join("pictures", "apple.png"))
        self.assets["candy"] = pygame.image.load(os.path.join("pictures", "lollipop.png"))

        # Scale them to fit cell size
        for key in self.assets:
            self.assets[key] = pygame.transform.scale(self.assets[key], (self.cell_size, self.cell_size))



    def render(self):
        if self.render_mode != "human":
            return super().render()

        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode(self.window_size)
            pygame.display.set_caption("CollectEnv GUI")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("Arial", 20)
    
        self.window.fill((255, 255, 255))  # tło
    
        # punkty
        score_text = self.font.render(f"Punkty: {self.score:.1f}", True, (0, 0, 0))
        self.window.blit(score_text, (10, 10))
    
        offset_y = 40  
    
        # Siatka
        for x in range(0, self.window_size[0], self.cell_size):
            pygame.draw.line(self.window, (200, 200, 200), (x, offset_y), (x, self.window_size[1]))
        for y in range(offset_y, self.window_size[1], self.cell_size):
            pygame.draw.line(self.window, (200, 200, 200), (0, y), (self.window_size[0], y))
    
        # Obiekty 
        for (x, y), item in self.objects.items():
            obj_type, _ = item
            sprite = self.assets["fruit"] if obj_type == "fruit" else self.assets["candy"]
            self.window.blit(sprite, (y * self.cell_size, x * self.cell_size + offset_y))
    
        # Agent 
        ax, ay = self.agent_pos
        self.window.blit(self.assets["agent"], (ay * self.cell_size, ax * self.cell_size + offset_y))
    
        pygame.display.flip()
        self.clock.tick(10)

    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None
