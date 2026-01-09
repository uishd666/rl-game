import os
import argparse
import glob
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import EvalCallback
from gridworld_env import GridWorldEnv

def train(map_dir, algorithm="ppo", timesteps=50000, save_path="models/"):
    """训练强化学习模型"""
    # 加载所有地图文件
    map_files = glob.glob(f"{map_dir}/*.txt")
    if not map_files:
        raise ValueError("未找到任何地图文件！")

    # 创建保存目录
    os.makedirs(save_path, exist_ok=True)

    for map_file in map_files:
        print(f"正在训练地图: {map_file}")
        
        # 创建环境
        env = GridWorldEnv(map_file=map_file)
        
        # 验证环境是否符合Gym标准
        check_env(env)
        
        # 选择算法
        if algorithm.lower() == "ppo":
            model = PPO("MlpPolicy", env, verbose=1, 
                        learning_rate=3e-4,
                        n_steps=2048,
                        batch_size=64,
                        n_epochs=10,
                        gamma=0.99)
        elif algorithm.lower() == "dqn":
            model = DQN("MlpPolicy", env, verbose=1,
                        learning_rate=1e-3,
                        batch_size=128,
                        gamma=0.99,
                        exploration_fraction=0.2,
                        exploration_final_eps=0.05)
        else:
            raise ValueError(f"不支持的算法: {algorithm}")
        
        # 评估回调
        eval_callback = EvalCallback(
            env,
            best_model_save_path=save_path,
            log_path="./logs/",
            eval_freq=5000,
            deterministic=True,
            render=False
        )
        
        # 训练模型
        print(f"开始使用 {algorithm.upper()} 训练...")
        model.learn(total_timesteps=timesteps, callback=eval_callback)
        
        # 保存最终模型
        final_path = os.path.join(save_path, f"{algorithm}_final_model_{os.path.basename(map_file).split('.')[0]}")
        model.save(final_path)
        print(f"模型已保存到: {final_path}")
        
        env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--map-dir", default="maps/", help="地图文件目录")
    parser.add_argument("--algo", default="ppo", choices=["ppo", "dqn"], help="算法")
    parser.add_argument("--timesteps", type=int, default=50000, help="训练步数")
    parser.add_argument("--save-path", default="models/", help="模型保存路径")
    
    args = parser.parse_args()
    train(args.map_dir, args.algo, args.timesteps, args.save_path)