import numpy as np
import matplotlib.pyplot as plt
import heapq
from tqdm import tqdm  # 引入进度条库

# 无人机A、B的位置和障碍圆的参数（与前述相同）
A = np.array([1000, 0])  # A的位置
B = np.array([-3500, 0])  # B的位置
C = np.array([0, 0])  # 障碍圆的中心
r = 500  # 障碍圆的半径

# 计算A到B直线与障碍圆的交点（与前述相同）
P_A = np.array([-500, 500 * np.sqrt(3)])  # 假设的交点，与A更近的交点
P_B = np.array([-500, -500 * np.sqrt(3)])  # 假设的交点，与B更近的交点

# 定义节点
nodes = {'A': A, 'P_A': P_A, 'B': B, 'P_B': P_B}

# 定义边及其权重
edges = [('A', 'P_A'), ('P_A', 'B'), ('B', 'P_B')]
edge_weights = {'A': np.linalg.norm(P_A - A), 'P_A': np.linalg.norm(B - P_A), 'B': np.linalg.norm(P_B - B), 'P_B': np.linalg.norm(A - P_B)}

# 构建无向图
graph = {node: {neighbor: edge_weights[neighbor] for neighbor in nodes if (node, neighbor) in edges or (neighbor, node) in edges} for node in nodes}

# 使用Dijkstra算法计算最短路径
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

# 使用Dijkstra算法计算无人机A的最短路径
shortest_path_A = dijkstra(graph, 'A')

# 使用Dijkstra算法计算无人机B的最短路径
shortest_path_B = dijkstra(graph, 'B')

# 生成A和B的优化航迹
optimized_path_A = [nodes['A']]
current_node = 'A'
for _ in tqdm(range(len(nodes) - 2)):  # 使用进度条
    next_node = min(graph[current_node], key=lambda node: shortest_path_A[node])
    optimized_path_A.append(nodes[next_node])
    current_node = next_node

optimized_path_B = [nodes['B']]
current_node = 'B'
for _ in tqdm(range(len(nodes) - 2)):  # 使用进度条
    next_node = min(graph[current_node], key=lambda node: shortest_path_B[node])
    optimized_path_B.append(nodes[next_node])
    current_node = next_node

# 将路径逆序，使其从A到B
optimized_path_A = np.array(optimized_path_A[::-1])
optimized_path_B = np.array(optimized_path_B[::-1])

# 绘制图形
fig, ax = plt.subplots()
ax.set_xlim(-4000, 1500)
ax.set_ylim(-2000, 2000)
obstacle = plt.Circle(C, r, color='r', fill=False)
ax.add_artist(obstacle)
ax.plot(optimized_path_A[:, 0], optimized_path_A[:, 1], marker='o', label='Drone A Optimized')
ax.plot(optimized_path_B[:, 0], optimized_path_B[:, 1], marker='x', label='Drone B Optimized')
ax.annotate('A', (A[0], A[1]), textcoords="offset points", xytext=(-15,5), ha='center', fontsize=10)
ax.annotate('B', (B[0], B[1]), textcoords="offset points", xytext=(-10,-15), ha='center', fontsize=10)
ax.legend()

# 显示绘图
plt.show()
