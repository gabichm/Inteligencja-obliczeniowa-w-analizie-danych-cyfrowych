import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import List, Tuple, Optional, Dict


class CollectEnv(gym.Env):

    metadata = {"render_modes": ["ansi"]}

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
        self.max_steps = 135
        self.start_pos = (10, 10)
        self.render_mode = render_mode

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Dict({
            "position": spaces.Box(low=0, high=19, shape=(2,), dtype=np.int32),
            "step": spaces.Discrete(self.max_steps + 1),
        })

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

        self.reset()

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.agent_pos = list(self.start_pos)
        self.current_step = 0
        self.score = 0
        self.objects: Dict[Tuple[int, int], str] = {}

        return self._get_obs(), {}

    def step(self, action: int):
        assert self.action_space.contains(action), f"Invalid action: {action}"

        # Spawn new objects
        for spawn_time, obj_type, pos in self.spawn_schedule:
            if spawn_time == self.current_step:
                self.objects[pos] = obj_type

        # Move agent
        delta = self.ACTION_MAP[action]
        new_row = min(max(self.agent_pos[0] + delta[0], 0), self.grid_size[0] - 1)
        new_col = min(max(self.agent_pos[1] + delta[1], 0), self.grid_size[1] - 1)
        self.agent_pos = [new_row, new_col]

        # Check for item pickup
        reward = 0
        pos_tuple = tuple(self.agent_pos)
        if pos_tuple in self.objects:
            if self.objects[pos_tuple] == "fruit":
                reward += 10
            elif self.objects[pos_tuple] == "candy":
                reward -= 10
            del self.objects[pos_tuple]

        # Action penalty
        if action in [0, 1, 2, 3]:  # up/down/left/right
            reward -= 0.2
        # "none" action has no penalty

        self.current_step += 1
        terminated = self.current_step >= self.max_steps

        return self._get_obs(), reward, terminated, False, {}

    def _get_obs(self):
        return {
            "position": np.array(self.agent_pos, dtype=np.int32),
            "step": self.current_step
        }

    def render(self):
        grid = [[" ." for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        for (x, y), item in self.objects.items():
            grid[x][y] = " F" if item == "fruit" else " C"
        ax, ay = self.agent_pos
        grid[ax][ay] = " A"
        output = "\n".join("".join(row) for row in grid)
        print(output)
        print(f"Step: {self.current_step}, Score: {self.score}")

    def close(self):
        pass
