import argparse
import time
import os
from stable_baselines3 import PPO, DQN
from gridworld_env import GridWorldEnv

def test(model_path, map_file, algorithm="ppo", episodes=5, save_dir="visualizations"):
    """测试训练好的模型"""
    # 加载模型
    if algorithm.lower() == "ppo":
        model = PPO.load(model_path)
    elif algorithm.lower() == "dqn":
        model = DQN.load(model_path)
    else:
        raise ValueError(f"不支持的算法: {algorithm}")
    
    # 创建环境
    env = GridWorldEnv(map_file=map_file, render_mode="human")
    
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    for episode in range(episodes):
        obs, _ = env.reset()
        done = False
        total_reward = 0
        steps = 0
        
        print(f"\n=== 回合 {episode + 1} ===")
        
        while not done:
            # 动作选择
            action, _states = model.predict(obs, deterministic=True)
            
            # 执行动作
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            total_reward += reward
            steps += 1
            
            # 渲染并保存图片
            save_path = os.path.join(save_dir, f"episode_{episode + 1}_step_{steps}.png")
            env.render(save_path=save_path)
            time.sleep(0.5)
        
        print(f"完成! 步数: {steps}, 总奖励: {total_reward:.2f}")
    
    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="模型文件路径")
    parser.add_argument("--map", default="maps/map.txt", help="地图文件路径")
    parser.add_argument("--algo", default="ppo", choices=["ppo", "dqn"], help="算法")
    parser.add_argument("--episodes", type=int, default=5, help="测试回合数")
    parser.add_argument("--save-dir", default="visualizations", help="可视化保存目录")
    
    args = parser.parse_args()
    test(args.model, args.map, args.algo, args.episodes, args.save_dir)