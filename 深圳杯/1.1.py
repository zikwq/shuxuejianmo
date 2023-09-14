import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

A = np.array([1, 0])
B = np.array([-3.5, 0])
C = np.array([0, 0])
r = 0.5
v = 0.1
r_a = 0.27


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


def generate_path_a(start, end, obstacle_center, obstacle_radius, extra_circle=False):
    if extra_circle:
        circle_center = np.array([1 + r_a, 0])
        theta_start = np.arctan2(start[1] - circle_center[1], start[0] - circle_center[0])
        theta_end = np.arctan2(y6 - circle_center[1], x6 - circle_center[0])

        # 确保逆时针运动
        if theta_end < theta_start:
            theta_end += 2 * np.pi

        theta = np.linspace(theta_start, theta_end,
                            int(r_a * np.abs(theta_end - theta_start) / v))
        circle_path = np.array([circle_center[0] + r_a * np.cos(theta),
                                circle_center[1] + r_a * np.sin(theta)]).T
        path1 = np.linspace(circle_path[-1], np.array([x5, y5]),
                            int(np.linalg.norm(circle_path[-1] - np.array([x5, y5])) / v))
        start = path1[-1]

    # 与B的轨迹相似
    start_tangent, _ = tangent_points(obstacle_center, obstacle_radius, start)
    _, end_tangent = tangent_points(obstacle_center, obstacle_radius, end)

    path2 = np.linspace(start, start_tangent, int(np.linalg.norm(start - start_tangent) / v))
    theta1 = np.arctan2(start_tangent[1] - obstacle_center[1], start_tangent[0] - obstacle_center[0])
    theta2 = np.arctan2(end_tangent[1] - obstacle_center[1], end_tangent[0] - obstacle_center[0])

    if theta1 < theta2:
        theta1, theta2 = theta2, theta1

    theta = np.linspace(theta2, theta1, int(obstacle_radius * np.abs(theta2 - theta1) / v))
    arc_path = np.array([obstacle_center[0] + obstacle_radius * np.cos(theta),
                         obstacle_center[1] + obstacle_radius * np.sin(theta)]).T
    path3 = np.linspace(arc_path[-1], end, int(np.linalg.norm(arc_path[-1] - end) / v))

    if extra_circle:
        return np.vstack([circle_path, path1, path2, arc_path, path3])
    else:
        return np.vstack([path2, arc_path, path3])


def generate_path_b(start, end, obstacle_center, obstacle_radius, extra_circle=False):
    original_start = np.copy(start)
    if extra_circle:
        circle_center = original_start + np.array([r_a, 0])
        theta = np.linspace(-np.pi, np.pi, int(2 * np.pi * r_a / v))
        extra_path = np.array([circle_center[0] + r_a * np.cos(theta),
                               circle_center[1] + r_a * np.sin(theta)]).T
        start = extra_path[-1]

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

    if extra_circle:
        return np.vstack([extra_path, path1, circle_path, path2])
    else:
        return np.vstack([path1, circle_path, path2])


# 计算用时
def compute_time(path, v):
    distances = np.sqrt(np.sum(np.diff(path, axis=0) ** 2, axis=1))
    total_distance = np.sum(distances)
    return total_distance / v
# 绘制障碍圆和a圆周的切点
def qiexian(x1, y1, x2, y2, r1, r2):
    d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # 外公切线交点与两圆心连线之间的夹角
    alpha = np.arctan2((r2 - r1), d)

    # 外公切线与两圆心连线的夹角
    theta = np.pi / 2 - alpha

    # 计算两条外公切线的端点
    x5, y5 = x1 - r1 * np.sin(alpha), y1 + r1 * np.cos(alpha)
    x6, y6 = x2 - r2 * np.sin(alpha), y2 + r2 * np.cos(alpha)

    return x5, y5, x6, y6


print("障碍圆和a圆周的切点", qiexian(0, 0, 1.3, 0, 0.5, r_a))
x5, y5, x6, y6=qiexian(0, 0, 1.3, 0, 0.5, r_a)

path_A = generate_path_a(A, B, C, r, extra_circle=True)
path_B = generate_path_b(B, A, C, r)

fig, ax = plt.subplots()
ax.set_xlim(-4, 2)
ax.set_ylim(-2, 2)

obstacle = plt.Circle(C, r, color='r')
ax.add_artist(obstacle)

line1, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
connection_line, = ax.plot([], [], 'k--', lw=1)
tangent_line, = ax.plot([], [], 'g--', lw=1)

T1a, T2a = tangent_points(C, r, A)
T1b, T2b = tangent_points(C, r, B)
ax.plot(*T1a, 'go')
ax.annotate("T1a", (T1a[0], T1a[1] + 0.1))
ax.plot(*T2a, 'go')
ax.annotate("T2a", (T2a[0], T2a[1] - 0.2))
ax.plot(*T1b, 'bo')
ax.annotate("T1b", (T1b[0], T1b[1] + 0.1))
ax.plot(*T2b, 'bo')
ax.annotate("T2b", (T2b[0], T2b[1] - 0.2))
ax.plot(*A, 'g*')
ax.annotate("A", (A[0], A[1] + 0.1))
ax.plot(*B, 'b*')
ax.annotate("B", (B[0], B[1] + 0.1))
plt.plot([x5, x6], [y5, y6], 'g--')




time_display = ax.text(0.05, 0.9, '', transform=ax.transAxes)
# 初始化飞机到达终点的标识
arrived_A = False
arrived_B = False
final_time_A = 0
final_time_B = 0


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    connection_line.set_data([], [])
    tangent_line.set_data([], [])
    time_display.set_text('')
    return line1, line2, connection_line, tangent_line, time_display


def animate(i):
    global arrived_A, arrived_B, final_time_A, final_time_B  # 使用全局变量

    if i < len(path_A):
        line1.set_data(path_A[:i, 0], path_A[:i, 1])
    if i >= len(path_A) and not arrived_A:  # 请注意这里的修改
        arrived_A = True
        final_time_A = compute_time(path_A, v)

    if i < len(path_B):
        line2.set_data(path_B[:i, 0], path_B[:i, 1])
    elif not arrived_B:
        arrived_B = True
        final_time_B = compute_time(path_B, v)

    if i < min(len(path_A), len(path_B)):
        connection_line.set_data([path_A[i, 0], path_B[i, 0]],
                                 [path_A[i, 1], path_B[i, 1]])

    if not arrived_B and i < len(path_B):
        _, tangent_point = tangent_points(C, r, path_B[i])
        tangent_slope = (tangent_point[1] - path_B[i, 1]) / (tangent_point[0] - path_B[i, 0])
        tangent_intercept = tangent_point[1] - tangent_slope * tangent_point[0]
        x_tangent = np.linspace(-4, 2, 2)
        y_tangent = tangent_slope * x_tangent + tangent_intercept
        tangent_line.set_data(x_tangent, y_tangent)

    elapsed_time_A = final_time_A if arrived_A else compute_time(path_A[:i + 1], v)
    elapsed_time_B = final_time_B if arrived_B else compute_time(path_B[:i + 1], v)
    time_display.set_text(f'Time A: {elapsed_time_A:.2f}s, Time B: {elapsed_time_B:.2f}s')

    return line1, line2, connection_line, tangent_line, time_display


ani = FuncAnimation(fig, animate, frames=max(len(path_A), len(path_B)), init_func=init,
                    repeat=False)  # 添加 repeat=False 参数
plt.show()


# 一些数据的打印
# 打印a的轨迹
def print_path_equations():
    # 1. 额外的圆周运动方程
    h = A[0] + 0.3
    k = A[1]
    r = 0.3
    print("下面是a的轨迹方程")
    print(f"1. Extra Circular Motion: (x - {h})^2 + (y - {k})^2 = {r ** 2}")

    # 2. 从圆周运动的结束点到障碍物的切点
    circle_end = np.array([h + r * np.cos(-np.pi), k + r * np.sin(-np.pi)])
    _, start_tangent = tangent_points(C, 0.5, circle_end)  # 修正此处，我们需要从右侧的切点开始
    x1, y1 = circle_end
    x2, y2 = _
    print(f"2. Line from Circle End to Tangent: (y - {y1}) / ({y2} - {y1}) = (x - {x1}) / ({x2} - {x1})")

    # 3. 沿着障碍物的圆周运动
    h, k = C
    r = 0.5
    print(f"3. Circle around Obstacle: (x - {h})^2 + (y - {k})^2 = {r ** 2}")

    # 4. 从障碍物的另一个切点到B的直线运动
    end_tangent, _ = tangent_points(C, 0.5, B)  # 修正此处，我们需要终止于左侧的切点
    x1, y1 = end_tangent
    x2, y2 = B
    print(f"4. Line from Tangent to B: (y - {y1}) / ({y2} - {y1}) = (x - {x1}) / ({x2} - {x1})")


# 在主程序中调用此函数
print(print_path_equations())


# 打印b的轨迹
def line_equation(p1, p2):
    """
    返回通过两点p1和p2的直线方程
    """
    x1, y1 = p1
    x2, y2 = p2

    if x2 - x1 == 0:  # Vertical line
        return f"x = {x1}"
    else:
        slope = (y2 - y1) / (x2 - x1)
        y_intercept = y1 - slope * x1
        return f"y = {slope}x + {y_intercept}"


def print_pathB_equations(path_B, C, r):
    # 1. 从B到障碍物的切点的直线
    _, start_tangent = tangent_points(C, r, B)  # 注意，这里我使用了tangent_points函数
    print("下面是b的轨迹方程")
    print(f"1. Line from B to Tangent: {line_equation(B, start_tangent)}")

    # 2. 沿着障碍物的圆周运动到另一个切点
    h, k = C
    print(f"2. Circle around Obstacle: (x - {h})^2 + (y - {k})^2 = {r ** 2}")

    # 3. 从障碍物的切点飞向A的直线
    # 这里我直接使用最后两个点，但是要确保path_B确实包括了无人机的整个轨迹
    print(f"3. Line from Tangent to A: {line_equation(path_B[-2], path_B[-1])}")


# 在主程序中调用此函数
print(print_pathB_equations(path_B, C, r))
print("a的切点：", T1a, T2a)
print("b的切点：", T1b, T2b)
