import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

A = np.array([1, 0])
B = np.array([-3.5, 0])
C = np.array([0, 0])
r = 0.5
v = 0.1  # 用于计算插值的步长


def tangent_points(C, r, P):
    OC = P - C
    distance_OP = np.linalg.norm(OC)
    cos_alpha = r / distance_OP
    sin_alpha = np.sqrt(1 - cos_alpha ** 2)
    x1 = C[0] + r * (OC[0] * cos_alpha - OC[1] * sin_alpha) / distance_OP
    y1 = C[1] + r * (OC[1] * cos_alpha + OC[0] * sin_alpha) / distance_OP
    x2 = C[0] + r * (OC[0] * cos_alpha + OC[1] * sin_alpha) / distance_OP
    y2 = C[1] + r * (OC[1] * cos_alpha - OC[0] * sin_alpha) / distance_OP
    return (x1, y1), (x2, y2)


# 生成飞行路径
def generate_path(start, end, obstacle_center, obstacle_radius):
    start_tangent, _ = tangent_points(obstacle_center, obstacle_radius, start)
    _, end_tangent = tangent_points(obstacle_center, obstacle_radius, end)

    path1 = np.linspace(start, start_tangent, int(np.linalg.norm(start - start_tangent) / v))
    theta1 = np.arctan2(start_tangent[1] - obstacle_center[1], start_tangent[0] - obstacle_center[0])
    theta2 = np.arctan2(end_tangent[1] - obstacle_center[1], end_tangent[0] - obstacle_center[0])

    if theta1 < theta2:
        theta1, theta2 = theta2, theta1

    theta = np.linspace(theta2, theta1, int(obstacle_radius * np.abs(theta2 - theta1) / v))
    circle_path = np.array([obstacle_center[0] + obstacle_radius * np.cos(theta),
                            obstacle_center[1] + obstacle_radius * np.sin(theta)]).T
    path2 = np.linspace(circle_path[-1], end, int(np.linalg.norm(circle_path[-1] - end) / v))
    return np.vstack([path1, circle_path, path2])


path_A = generate_path(A, B, C, r)
path_B = generate_path(B, A, C, r)

def symmetric_point_on_tangent(tangent_point, B_point):
    dx = B_point[0] - tangent_point[0]
    dy = B_point[1] - tangent_point[1]

    symmetric_x = tangent_point[0] - dx
    symmetric_y = tangent_point[1] - dy

    return symmetric_x, symmetric_y

# 动画部分
fig, ax = plt.subplots()
ax.set_xlim(-4, 2)
ax.set_ylim(-2, 2)
obstacle = plt.Circle(C, r, color='r')
ax.add_artist(obstacle)
line1, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
connection_line, = ax.plot([], [], 'k--', lw=1)
tangent_line, = ax.plot([], [], 'g--', lw=1)
symmetric_point_plot, = ax.plot([], [], 'bo', markersize=8)  # 新增对称点

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    connection_line.set_data([], [])
    tangent_line.set_data([], [])
    symmetric_point_plot.set_data([], [])  # 初始化对称点数据
    return line1, line2, connection_line, tangent_line, symmetric_point_plot

def animate(i):
    if i < len(path_A):
        line1.set_data(path_A[:i, 0], path_A[:i, 1])
    if i < len(path_B):
        line2.set_data(path_B[:i, 0], path_B[:i, 1])

    if i < min(len(path_A), len(path_B)):
        connection_line.set_data([path_A[i, 0], path_B[i, 0]],
                                 [path_A[i, 1], path_B[i, 1]])

    # 绘制B无人机与上半圆的切线
    if i < len(path_B):
        _, tangent_point = tangent_points(C, r, path_B[i])
        tangent_slope = (tangent_point[1] - path_B[i, 1]) / (tangent_point[0] - path_B[i, 0])
        tangent_intercept = tangent_point[1] - tangent_slope * tangent_point[0]
        x_tangent = np.linspace(-4, 2, 2)
        y_tangent = tangent_slope * x_tangent + tangent_intercept
        tangent_line.set_data(x_tangent, y_tangent)

        # 绘制对称点
        symmetric_x, symmetric_y = symmetric_point_on_tangent(tangent_point, path_B[i])
        symmetric_point_plot.set_data(symmetric_x, symmetric_y)

    return line1, line2, connection_line, tangent_line, symmetric_point_plot

ani = FuncAnimation(fig, animate, frames=max(len(path_A), len(path_B)), init_func=init, blit=True)
plt.show()