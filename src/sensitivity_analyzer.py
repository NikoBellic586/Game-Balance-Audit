import random
import matplotlib.pyplot as plt # 以后生成报告用

class Role:
    def __init__(self, name, hp, atk, defense=0, speed=10):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense  # 新增防御力
        self.speed = speed      # 新增速度（决定谁先手）

def simulate_once(a, b):
    hp_a, hp_b = a.hp, b.hp
    # 速度快者先手
    first, second = (a, b) if a.speed >= b.speed else (b, a)
    hp_first, hp_second = (hp_a, hp_b) if a.speed >= b.speed else (hp_b, hp_a)

    while hp_first > 0 and hp_second > 0:
        # 第一人攻击，考虑防御力减伤（最低伤害为1）
        dmg = max(1, first.atk - second.defense)
        hp_second -= dmg
        if hp_second <= 0: return first.name
        
        # 第二人反击
        dmg = max(1, second.atk - first.defense)
        hp_first -= dmg
        if hp_first <= 0: return second.name

def get_win_rate(role_a, role_b, n=10000):
    a_wins = sum(1 for _ in range(n) if simulate_once(role_a, role_b) == role_a.name)
    return a_wins / n

def find_balance_point(player, boss, target_win_rate=0.5):
    """
    【核心算法】自动寻找平衡点
    不断微调 player 的攻击力，直到胜率接近 target_win_rate
    """
    print(f"--- EquiliLogic 自动平衡审计中 ---")
    current_atk = player.atk
    step = 1
    
    for i in range(20): # 最多迭代20次
        wr = get_win_rate(player, boss)
        print(f"迭代 {i}: 当攻击力为 {current_atk} 时, 玩家胜率为 {wr:.2%}")
        
        if abs(wr - target_win_rate) < 0.02:
            print(f"✅ 找到理想平衡数值！建议攻击力设定为: {current_atk}")
            return current_atk
        
        # 简单的梯度调节逻辑
        if wr > target_win_rate:
            current_atk -= step
        else:
            current_atk += step
        player.atk = current_atk
    
    print("⚠️ 未能在迭代内找到完美平衡，请考虑大幅度调整数值结构。")

if __name__ == "__main__":
    # 定义一个过于强大的 BOSS
    boss_char = Role("魔王", hp=500, atk=50, defense=10, speed=5)
    # 玩家角色
    hero_char = Role("勇者", hp=200, atk=30, defense=5, speed=12)
    
    find_balance_point(hero_char, boss_char)
