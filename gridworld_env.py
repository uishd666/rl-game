import gymnasium as gym
import numpy as np
from gymnasium import spaces
import os
import matplotlib.pyplot as plt

class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    
    def __init__(self, map_file="maps/map.txt", render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        
        # 加载地图
        self.grid_map, self.start_pos, self.end_pos = self._load_map(map_file)
        self.height, self.width = self.grid_map.shape
        
        # 定义状态空间 (agent位置)
        self.observation_space = spaces.Box(
            low=np.array([0, 0], dtype=np.int32),
            high=np.array([self.height-1, self.width-1], dtype=np.int32),
            dtype=np.int32
        )
        
        # 定义动作空间: 0=上, 1=下, 2=左, 3=右
        self.action_space = spaces.Discrete(4)
        
        # 动作到位置变化的映射
        self.action_to_delta = {
            0: np.array([-1, 0]),  # 上
            1: np.array([1, 0]),   # 下
            2: np.array([0, -1]),  # 左
            3: np.array([0, 1])    # 右
        }
        
        self.current_pos = None
        self.step_count = 0
        self.max_steps = self.height * self.width * 2  # 最大步数限制
    
    def _load_map(self, map_file):
        """加载地图文件"""
        if not os.path.exists(map_file):
            raise FileNotFoundError(f"地图文件不存在: {map_file}")
        
        with open(map_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        grid = []
        start_pos = None
        end_pos = None
        
        for i, line in enumerate(lines):
            row = []
            for j, char in enumerate(line):
                if char == '*':
                    row.append(0)  # 空地
                elif char == '#':
                    row.append(1)  # 障碍物
                elif char == '@':
                    row.append(0)
                    start_pos = np.array([i, j], dtype=np.int32)
                elif char == '$':
                    row.append(0)
                    end_pos = np.array([i, j], dtype=np.int32)
                else:
                    raise ValueError(f"无效的地图字符 '{char}' 在位置 ({i}, {j})")
            grid.append(row)
        
        if start_pos is None or end_pos is None:
            raise ValueError("地图必须包含起点 '@' 和终点 '$'")
        
        return np.array(grid, dtype=np.int32), start_pos, end_pos
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_pos = self.start_pos.copy()
        self.step_count = 0
        
        return self._get_obs(), {}
    
    def _get_obs(self):
        """获取当前状态观测"""
        return self.current_pos.copy()
    
    def step(self, action):
        """执行动作并返回结果"""
        self.step_count += 1
        
        # 计算新位置
        delta = self.action_to_delta[action]
        new_pos = self.current_pos + delta
        
        # 检查边界和障碍物
        terminated = False
        truncated = False
        reward = -0.1  # 每步的小惩罚，鼓励最短路径
        
        # 检查是否越界或撞墙
        if (new_pos[0] < 0 or new_pos[0] >= self.height or
            new_pos[1] < 0 or new_pos[1] >= self.width or
            self.grid_map[new_pos[0], new_pos[1]] == 1):  # 障碍物
            # 撞墙或越界，位置不变，给予惩罚
            reward = -1.0
        else:
            self.current_pos = new_pos
        
        # 检查是否到达终点
        if np.array_equal(self.current_pos, self.end_pos):
            reward = 10.0
            terminated = True
        
        # 检查是否超过最大步数
        if self.step_count >= self.max_steps:
            truncated = True
        
        return self._get_obs(), reward, terminated, truncated, {}
    
    def render(self, save_path=None):
        """渲染当前状态"""
        if self.render_mode is None:
            return None

        # 创建可视化地图
        viz_map = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if self.grid_map[i, j] == 1:
                    row.append('#')
                elif np.array_equal([i, j], self.current_pos):
                    row.append('A')  # Agent当前位置
                elif np.array_equal([i, j], self.start_pos):
                    row.append('@')
                elif np.array_equal([i, j], self.end_pos):
                    row.append('$')
                else:
                    row.append('*')
            viz_map.append(''.join(row))

        if save_path:
            # 保存为图片
            plt.figure(figsize=(8, 8))
            for i, row in enumerate(viz_map):
                for j, char in enumerate(row):
                    color = "white"
                    if char == '#':
                        color = "black"
                    elif char == 'A':
                        color = "blue"
                    elif char == '@':
                        color = "green"
                    elif char == '$':
                        color = "red"
                    plt.gca().add_patch(plt.Rectangle((j, self.height - i - 1), 1, 1, color=color))
            plt.xlim(0, self.width)
            plt.ylim(0, self.height)
            plt.axis("off")
            plt.savefig(save_path)
            plt.close()

        print("\n".join(viz_map))
        print("-" * self.width)
        return viz_map
    
    def close(self):
        pass