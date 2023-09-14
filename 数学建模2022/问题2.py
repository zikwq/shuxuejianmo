import numpy as np
import matplotlib.pyplot as plt

# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

K = 0.1  # 弹簧常数

def adjust_positions(drones_positions, ideal_positions, K, iterations=1000):
    adjusted_positions = drones_positions.copy()

    for _ in range(iterations):
        for i in range(len(adjusted_positions)):
            r, theta = adjusted_positions[i]
            r_ideal, theta_ideal = ideal_positions[i]
            force = K * (r_ideal - r)
            adjusted_positions[i] = (r + force, theta)

    return adjusted_positions

def plot_drones(positions, color='r', marker='o', label=None):
    x_coords = [r * np.cos(np.deg2rad(theta)) for r, theta in positions]
    y_coords = [r * np.sin(np.deg2rad(theta)) for r, theta in positions]
    plt.scatter(x_coords, y_coords, color=color, marker=marker, label=label)

# 初始化无人机位置（这里是示例，实际数据可能不同）
initial_positions = [
    (0, 0), (50, 0), (100, 40), (150, 80), (200, 120),
    (250, 160), (300, 200), (350, 240), (400, 280), (450, 320)
]

# 确定锥形编队的理想位置
spacing = 50
ideal_positions = [(i*spacing, i*40) for i in range(10)]

adjusted_positions = adjust_positions(initial_positions, ideal_positions, K)

plt.figure(figsize=(10, 10))
plot_drones(initial_positions, color='r', marker='o', label='初始位置')
plot_drones(adjusted_positions, color='b', marker='s', label='调整后的位置')
plot_drones(ideal_positions, color='g', marker='x', label='理想位置')

plt.legend(loc="upper left")
plt.title("锥形编队的无人机位置调整")
plt.xlabel("X坐标 (m)")
plt.ylabel("Y坐标 (m)")
plt.grid(True)
plt.show()
