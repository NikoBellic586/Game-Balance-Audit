import networkx as nx
import matplotlib.pyplot as plt

# 设置绘图字体
plt.rcParams['font.sans-serif'] = ['SimHei'] 

class ScriptAuditor:
    def __init__(self):
        # 创建一个有向图
        self.G = nx.DiGraph()

    def add_logic_flow(self, from_node, to_node, description=""):
        """添加逻辑流：从一个线索指向另一个线索"""
        self.G.add_edge(from_node, to_node, label=description)

    def perform_audit(self, start_node, end_node):
        print(f"--- EquiliLogic 剧情逻辑审计开始 ---")
        
        # 1. 检测不可达节点 (无效线索)
        # 即：从起点出发，无论如何也找不到的线索
        all_nodes = set(self.G.nodes())
        reachable_nodes = nx.descendants(self.G, start_node) | {start_node}
        unreachable = all_nodes - reachable_nodes
        
        if unreachable:
            print(f"⚠️ 发现无效线索 (孤立点): {unreachable}")
            print(f"   建议：增加通往这些线索的提示，否则玩家永远无法发现它们。")
        else:
            print(f"✅ 所有线索均可触达。")

        # 2. 检测逻辑死路 (Sink Nodes)
        # 即：除了真相(终点)以外，哪些点进去后就没路了
        dead_ends = [node for node in self.G.nodes() 
                     if self.G.out_degree(node) == 0 and node != end_node]
        
        if dead_ends:
            print(f"❌ 发现逻辑死路 (玩家会卡死在这里): {dead_ends}")
            print(f"   建议：为这些节点增加后续逻辑出口。")
        else:
            print(f"✅ 未发现逻辑死路。")

        # 3. 检测是否能到达真相
        if nx.has_path(self.G, start_node, end_node):
            path = nx.shortest_path(self.G, start_node, end_node)
            print(f"✅ 逻辑闭环验证成功！通往真相的最短路径为: {' -> '.join(path)}")
        else:
            print(f"🚨 重大逻辑漏洞：从起点无法到达真相！剧本无法通关。")

    def visualize(self):
        """可视化逻辑拓扑图"""
        pos = nx.spring_layout(self.G)
        plt.figure(figsize=(12, 8))
        nx.draw(self.G, pos, with_labels=True, node_size=2000, 
                node_color='lightblue', font_size=10, font_weight='bold', 
                arrows=True, arrowsize=20)
        
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        
        plt.title("剧本逻辑拓扑审计图", fontsize=15)
        plt.show()

if __name__ == "__main__":
    auditor = ScriptAuditor()

    # 案例：模拟一个有漏洞的剧本
    # 节点：起跑点, 尸检报告, 凶器, 嫌疑人A, 秘密地下室, 真相
    auditor.add_logic_flow("尸检报告", "凶器", "发现伤口形状")
    auditor.add_logic_flow("起跑点", "尸检报告", "第一现场调查")
    auditor.add_logic_flow("嫌疑人A", "真相", "指认凶手")
    auditor.add_logic_flow("凶器", "秘密地下室", "通过编号找到出处")
    
    # 注意：这里我们故意没连通 "秘密地下室" 到 "嫌疑人A"
    # 同时增加一个没人能找到的孤立线索 "陈年旧照"
    auditor.G.add_node("陈年旧照") 

    auditor.perform_audit(start_node="起跑点", end_node="真相")
    auditor.visualize()
