import random
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体（防止图片中文乱码，如果是Mac系统需换成 'Arial Unicode MS'）
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

class Role:
    def __init__(self, name, hp, atk, defense=5):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense

def simulate_win_rate(player_atk, boss, n=2000):
    """计算特定攻击力下的胜率"""
    player = Role("勇者", hp=200, atk=player_atk)
    wins = 0
    for _ in range(n):
        hp_p, hp_b = player.hp, boss.hp
        while hp_p > 0 and hp_b > 0:
            hp_b -= max(1, player.atk - boss.defense)
            if hp_b <= 0: wins += 1; break
            hp_p -= max(1, boss.atk - player.defense)
    return wins / n

def generate_audit_report():
    boss = Role("魔王", hp=500, atk=40, defense=10)
    
    # 设定审计范围：攻击力从 10 变化到 70
    atk_range = np.arange(10, 71, 2)
    win_rates = []

    print("正在生成压力测试数据...")
    for atk in atk_range:
        wr = simulate_win_rate(atk, boss)
        win_rates.append(wr)
        print(f"测试攻击力 {atk}: 胜率 {wr:.2%}")

    # --- 开始绘图 ---
    plt.figure(figsize=(10, 6))
    plt.plot(atk_range, win_rates, marker='o', linestyle='-', color='b', label='胜率曲线')
    
    # 绘制 50% 平衡线
    plt.axhline(y=0.5, color='r', linestyle='--', label='绝对平衡线 (50%)')
    
    # 标注平衡区间 (45%-55%)
    plt.fill_between(atk_range, 0.45, 0.55, color='green', alpha=0.2, label='理想平衡区间')

    plt.title("“衡逻辑”数值平衡审计报告 - 勇者 vs 魔王", fontsize=14)
    plt.xlabel("玩家初始攻击力 (ATK)", fontsize=12)
    plt.ylabel("预期胜率 (Win Rate)", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 自动识别平衡点并标注
    idx = (np.abs(np.array(win_rates) - 0.5)).argmin()
    balance_atk = atk_range[idx]
    plt.annotate(f'建议平衡点: ATK={balance_atk}', 
                 xy=(balance_atk, win_rates[idx]), 
                 xytext=(balance_atk+5, win_rates[idx]-0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.savefig('audit_report_sample.png') # 保存结果图
    print("\n✅ 审计图表已生成：audit_report_sample.png")
    plt.show()

if __name__ == "__main__":
    generate_audit_report()
