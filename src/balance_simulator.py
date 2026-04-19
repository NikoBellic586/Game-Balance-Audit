import random
import time

class Role:
    """定义游戏角色属性"""
    def __init__(self, name, hp, atk, crit_rate=0.0):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.crit_rate = crit_rate

def simulate_battle(role_a, role_b):
    """模拟单场对局，返回胜者名字"""
    hp_a, hp_b = role_a.hp, role_b.hp
    
    # 模拟回合制战斗
    while hp_a > 0 and hp_b > 0:
        # A 攻击 B
        damage_a = role_a.atk * (2 if random.random() < role_a.crit_rate else 1)
        hp_b -= damage_a
        if hp_b <= 0: return role_a.name
        
        # B 攻击 A
        damage_b = role_b.atk * (2 if random.random() < role_b.crit_rate else 1)
        hp_a -= damage_b
        if hp_a <= 0: return role_b.name

def monte_carlo_audit(role_1, role_2, n_simulations=1000000):
    """
    核心算法：执行 N 次模拟，计算胜率分布 P(Wi)
    """
    print(f"--- EquiliLogic 数值审计开始 ---")
    print(f"正在对 [{role_1.name}] vs [{role_2.name}] 进行 {n_simulations} 次模拟...")
    
    start_time = time.time()
    results = {role_1.name: 0, role_2.name: 0}
    
    for _ in range(n_simulations):
        winner = simulate_battle(role_1, role_2)
        results[winner] += 1
    
    end_time = time.time()
    
    # 计算胜率 P(Wi)
    p1 = results[role_1.name] / n_simulations
    p2 = results[role_2.name] / n_simulations
    
    print(f"审计完成！耗时: {end_time - start_time:.2f} 秒")
    print(f"胜率分布: \n - {role_1.name}: {p1:.2%}\n - {role_2.name}: {p2:.2%}")
    
    # 逻辑审计标准：偏差 σ > 5% 触发预警
    deviation = abs(p1 - 0.5)
    if deviation > 0.05:
        print(f"❌ 警告：数值严重不平衡！偏差值 {deviation:.2%} > 5%")
        print(f"建议：调低 {role_1.name if p1 > p2 else role_2.name} 的攻击力或生命值。")
    else:
        print(f"✅ 检查通过：数值平衡，偏差值 {deviation:.2%} 在安全范围内。")

# --- 实例测试 (对应计划书中的数值崩坏痛点) ---
if __name__ == "__main__":
    # 模拟一个“过于强大”的刺客角色 vs 平衡角色
    assassin = Role("暗影刺客", hp=80, atk=25, crit_rate=0.3)
    warrior = Role("平民战士", hp=120, atk=15, crit_rate=0.05)
    
    monte_carlo_audit(assassin, warrior)
