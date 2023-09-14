# Reload the necessary libraries and data
import matplotlib.pyplot as plt
import networkx as nx
# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# Create a new directed graph
G = nx.DiGraph()

# Define the nodes for our process
nodes = [
    "1. 加载数据",
    "2. 坐标转化",
    "3. 计算深度对应的覆盖宽度",
    "4. 定义计算函数",
    "5. 调用贪婪算法生成路径",
    "6. 计算测量线的总长度",
    "7. 计算漏测海域的百分比",
    "8. 绘制深度分布与调整后的密集贪婪测量线",
    "9. 计算平均深度",
    "10. 输出"
]

greedy_nodes_updated = [
    "定义计算函数",
    "选择下一个路径点",
    "使用调整的贪婪算法生成路径",
    "计算测量线的总长度",
    "计算漏测海域的百分比",
    "计算重叠率超过20%的部分的总长度"
]
# Add nodes to the graph
for node in nodes:
    G.add_node(node)

# Define the edges based on the order of operations in the code
edges = [
    (nodes[0], nodes[1]),
    (nodes[1], nodes[2]),
    (nodes[2], nodes[3]),
    (nodes[3], nodes[4]),
    (nodes[4], nodes[5]),
    (nodes[5], nodes[6]),
    (nodes[6], nodes[7]),
    (nodes[7], nodes[8]),
    (nodes[8], nodes[9])
]

# Add edges to the graph
G.add_edges_from(edges)

# Draw the graph
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000, font_size=12, font_weight='bold', edge_color="gray")
nx.draw_networkx_edge_labels(G, pos, edge_labels={(nodes[i], nodes[i+1]): str(i+2) for i in range(len(nodes)-1)})
plt.title("Flowchart of the Code Process")
plt.axis('off')
plt.tight_layout()
plt.show()





# Updated nodes for the detailed greedy algorithm process in Chinese
greedy_nodes_chinese = [
    "1. 定义相关计算函数",
    "2. 开始贪婪选择",
    "3. 检查是否到达边界",
    "3a. 转向并移动到下一个纬度",
    "3b. 继续向前移动",
    "4. 使用调整的贪婪算法生成路径",
    "5. 计算测量线的总长度",
    "6. 计算漏测海域的百分比",
    "7. 计算重叠率超过20%的部分的总长度"
]

# Create a new directed graph for the detailed greedy algorithm in Chinese
G_greedy_chinese = nx.DiGraph()

# Add nodes to the graph
for node in greedy_nodes_chinese:
    G_greedy_chinese.add_node(node)

# Define the edges based on the detailed order of operations in the greedy algorithm
greedy_edges_chinese = [
    (greedy_nodes_chinese[0], greedy_nodes_chinese[1]),
    (greedy_nodes_chinese[1], greedy_nodes_chinese[2]),
    (greedy_nodes_chinese[2], greedy_nodes_chinese[3]),
    (greedy_nodes_chinese[2], greedy_nodes_chinese[4]),
    (greedy_nodes_chinese[3], greedy_nodes_chinese[4]),
    (greedy_nodes_chinese[4], greedy_nodes_chinese[5]),
    (greedy_nodes_chinese[5], greedy_nodes_chinese[6]),
    (greedy_nodes_chinese[6], greedy_nodes_chinese[7]),
    (greedy_nodes_chinese[7], greedy_nodes_chinese[8])
]

# Add edges to the graph
G_greedy_chinese.add_edges_from(greedy_edges_chinese)

# Set positions for nodes in a shell layout
shell_pos_chinese = nx.shell_layout(G_greedy_chinese)

# Draw the graph using the shell layout
plt.figure(figsize=(14, 10))
nx.draw(G_greedy_chinese, shell_pos_chinese, with_labels=True, node_shape='s', node_color="lightcoral", node_size=3500, font_size=12, font_weight='bold', edge_color="gray")
plt.title("贪婪算法流程图")
plt.axis('off')
plt.show()
