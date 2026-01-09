# RL GridWorld Game

A reinforcement learning project for grid world navigation using Stable Baselines3.

## Overview

Train AI agents to navigate through grid-based mazes using PPO and DQN algorithms. The agent learns to find the shortest path from start (@) to goal ($) while avoiding obstacles (#).

## Features

- **Multiple Algorithms**: Supports PPO and DQN reinforcement learning algorithms
- **Custom Maps**: Various difficulty levels (easy, medium, hard) with different maze layouts
- **Real-time Training**: Visualize training progress and agent behavior
- **Model Persistence**: Save and load trained models for evaluation

## Quick Start

1. **Install Dependencies**:
```bash
pip install stable-baselines3 gymnasium matplotlib numpy
```

2. **Train a Model**:
```bash
python train.py --map-dir maps/ --algo ppo --timesteps 50000
```

3. **Test the Model**:
```bash
python test.py --map map.txt --model model.zip
```

## Project Structure

```
├── gridworld_env.py # Custom grid world environment
├── train.py # Training script ├── test.py # Testing and evaluation
├── maps/ # Maze map files
├── models/ # Saved trained models
└── logs/ # Training logs
```

## Map Format

Maps use simple text-based format:
- `@` - Start position
- `$` - Goal position  
- `#` - Obstacle
- `*` - Free space