import numpy as np
import matplotlib.pyplot as plt

# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义绘制无人机位置的函数
def plot_drones(positions, color='r', marker='o', label=None, s=None):
    # 将极坐标转换为直角坐标
    x_coords = [r * np.cos(np.radians(theta)) for r, theta in positions]
    y_coords = [r * np.sin(np.radians(theta)) for r, theta in positions]
    # 根据需要绘制散点图
    if s is None:
        plt.scatter(x_coords, y_coords, color=color, marker=marker, label=label)
    else:
        plt.scatter(x_coords, y_coords, color=color, marker=marker, s=s, label=label)

# 计算两个无人机之间的角度
def compute_angles_between_drones(ref_positions, target_position):
    angles = []
    for pos in ref_positions:
        # 使用反正切函数计算角度
        angle = np.arctan2(target_position[0] * np.sin(np.radians(target_position[1])) - pos[0] * np.sin(np.radians(pos[1])),
                           target_position[0] * np.cos(np.radians(target_position[1])) - pos[0] * np.cos(np.radians(pos[1])))
        angles.append(np.degrees(angle))  # 将弧度转换为角度
    return angles

# 找到与目标角度最接近的理想角度
def find_best_match(angles, ideal_angles_list):
    # 计算角度差的总和，选取最小差的角度
    diffs = [sum(np.abs(np.array(angles) - np.array(ideal_angles))) for ideal_angles in ideal_angles_list]
    return np.argmin(diffs)

# 计算初始位置和发射无人机之间的角度
initial_positions = [(0, 0), (100, 0), (98, 40.1), (112, 80.21), (105, 119.75), (98, 159.86), (112, 199.96), (105, 240.07), (98, 280.17), (112, 320.28)]
# 计算平均半径，排除圆心
avg_radius = np.mean([pos[0] for pos in initial_positions if pos[0] != 0])
ideal_positions = [(0, 0)]  # 初始化理想位置

# 根据角度计算理想位置
for i in range(1, 10):
    angle = i * 40
    ideal_positions.append((100, angle))  # 所有理想位置半径都为100，只调整角度

# 设置发射信号无人机的位置
signal_drones = [(0, 0), initial_positions[1], initial_positions[7]]

# 计算每个理想位置与发射信号无人机之间的角度
ideal_angles_list = [compute_angles_between_drones(signal_drones, ideal_pos) for ideal_pos in ideal_positions]

# 初始化调整后位置列表，初始位置无需调整
adjusted_positions = [initial_positions[0]]

# 对每个初始位置无人机进行调整
for pos in initial_positions[1:]:
    angles = compute_angles_between_drones(signal_drones, pos)  # 计算角度
    best_match_idx = find_best_match(angles, ideal_angles_list)  # 找到最接近的理想角度
    adjusted_positions.append(ideal_positions[best_match_idx])  # 添加调整后位置

# 绘制图形
plt.figure(figsize=(10, 10))
plot_drones(initial_positions, color='r', marker='o', label='初始位置')
plot_drones(adjusted_positions, color='b', marker='s', label='调整后的位置')
plot_drones(signal_drones, color='y', marker='*', s=150, label='发射信号的飞机')
plot_drones(ideal_positions, color='g', marker='x', label='理想位置')
plt.legend(loc="upper left")
plt.title("无人机位置调整")
plt.xlabel("X坐标 (m)")
plt.ylabel("Y坐标 (m)")
plt.grid(True)
plt.show()

# 打印结果
print("初始位置", initial_positions)
print("理想位置", ideal_positions)
print("调整后位置", adjusted_positions)
