#!/usr/bin/env python3
"""
迷宫地图一键生成脚本（修复版）
所有地图都已修正为矩形格式
"""

# 修复后的地图数据 - 确保每行长度一致
maps = {
    # 简单迷宫 (已修复)
    "map_easy_1.txt": ["@**", 
                       "*#$", 
                       "***"],
    
    "map_easy_2.txt": ["@***", 
                       "*##*", 
                       "**#*", 
                       "***$"],
    
    "map_easy_3.txt": ["@**#", 
                       "*#*#", 
                       "**#*", 
                       "##*$"],
    
    "map_easy_4.txt": ["@***#", 
                       "*#*#*", 
                       "**#*$"],
    
    "map_easy_5.txt": ["@****", 
                       "*##*#", 
                       "**#*#", 
                       "***#$"],
    
    # 中等迷宫 (已修复)
    "map_medium_1.txt": ["@*****", 
                         "*###**", 
                         "**#*#*", 
                         "*#**#*", 
                         "****#$"],
    
    "map_medium_2.txt": ["@******", 
                         "*##*###", 
                         "**#**#*", 
                         "*#*#**#", 
                         "*****#$"],
    
    "map_medium_3.txt": ["@*******", 
                         "*###**#*", 
                         "**#**#**", 
                         "*#**###*", 
                         "**#**#**", 
                         "******#$"],
    
    "map_medium_4.txt": ["@********", 
                         "*####**#*", 
                         "**#**#*#*", 
                         "*#****#**", 
                         "*****##$*"],  # 修复：最后加一个*
    
    "map_medium_5.txt": ["@******", 
                         "*##*###", 
                         "**#**#*", 
                         "*#*#**#", 
                         "**#**#*", 
                         "*###**#", 
                         "*****#$"],
    
    # 复杂迷宫 (已修复)
    "map_hard_1.txt": ["@********", 
                       "*####**#*", 
                       "**#**#*#*", 
                       "*#****#**", 
                       "**#**###*", 
                       "*#**#**#*", 
                       "**#**#**#", 
                       "*###**#**", 
                       "*******$*"],  # 修复：最后加一个*
    
    "map_hard_2.txt": ["@**********", 
                       "*########**",  # 修复：最后加一个*
                       "**#**#**#**", 
                       "*#*****#**#",  # 修复：最后加一个#
                       "**#**###**#", 
                       "*#**#**#*#*", 
                       "**#**#**#**", 
                       "*########**",  # 修复：最后加一个*
                       "********#$*"],  # 修复：最后加一个*
    
    "map_hard_3.txt": ["@***********", 
                       "*#########**",  # 修复：最后加一个*
                       "**#**#**#**#", 
                       "*#*******#**", 
                       "**#**###**#*", 
                       "*#**#**#**#*", 
                       "**#**#**#**#", 
                       "*#**#**#**#*", 
                       "**#**#**#**#", 
                       "*#########**",  # 修复：最后加一个*
                       "**********$*"],  # 修复：最后加一个*
}

def check_map_integrity():
    """检查所有地图的完整性"""
    print("检查地图完整性...")
    all_good = True
    
    for filename, map_data in maps.items():
        # 检查行长度是否一致
        row_lengths = [len(row) for row in map_data]
        if len(set(row_lengths)) > 1:
            print(f"❌ {filename}: 行长度不一致 {row_lengths}")
            all_good = False
            continue
        
        # 检查起点和终点数量
        start_count = sum(row.count('@') for row in map_data)
        end_count = sum(row.count('$') for row in map_data)
        
        if start_count != 1:
            print(f"❌ {filename}: 起点数量错误 ({start_count}个)")
            all_good = False
        
        if end_count != 1:
            print(f"❌ {filename}: 终点数量错误 ({end_count}个)")
            all_good = False
        
        # 检查地图是否连通（简单检查至少有一条路径）
        # 这里只是简单检查，不进行完整路径搜索
        
        if all_good:
            print(f"✅ {filename}: 格式正确 ({row_lengths[0]}x{len(map_data)})")
    
    return all_good

def create_maps():
    """创建所有地图文件"""
    # 首先检查地图完整性
    if not check_map_integrity():
        print("\n⚠️  发现地图格式问题，请先修复!")
        return
    
    import os
    
    # 创建maps文件夹
    os.makedirs("maps", exist_ok=True)
    
    # 生成所有地图文件
    created_count = 0
    for name, data in maps.items():
        filepath = os.path.join("maps", name)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(data))
        
        # 显示地图信息
        width = len(data[0]) if data else 0
        height = len(data)
        print(f"✓ 已创建: maps/{name} ({width}x{height})")
        created_count += 1
    
    print(f"\n✅ 完成！共创建 {created_count} 个迷宫地图文件。")
    print(f"地图文件保存在 'maps' 文件夹中。")
    
    # 创建汇总文件
    # create_summary_file()

def create_summary_file():
    """创建汇总文件"""
    import os
    
    with open("maps_summary.txt", 'w', encoding='utf-8') as f:
        f.write("迷宫地图汇总\n")
        f.write("=" * 50 + "\n\n")
        
        for filename, map_data in maps.items():
            f.write(f"文件名: {filename}\n")
            f.write(f"尺寸: {len(map_data[0])}x{len(map_data)}\n")
            f.write("地图:\n")
            f.write("-" * 40 + "\n")
            
            for row in map_data:
                f.write(row + "\n")
            
            f.write("\n" + "=" * 50 + "\n\n")
    
    print("✓ 已创建地图汇总文件: maps_summary.txt")

if __name__ == "__main__":
    print("迷宫地图生成器 (修复版)")
    print("=" * 40)
    
    # 创建地图文件
    create_maps()