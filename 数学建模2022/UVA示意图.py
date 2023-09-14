# 显示题目要求的图形
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from matplotlib.patches import Arc

# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def draw_angle_annotation(ax, center, start, end, radius=15, text_offset=20, color="black"):
    # 绘制一个弧线表示角度
    arc = Arc(center, radius, radius, angle=0,
              theta1=math.degrees(math.atan2(start[1] - center[1], start[0] - center[0])),
              theta2=math.degrees(math.atan2(end[1] - center[1], end[0] - center[0])), color=color)
    ax.add_patch(arc)

    # 为弧线中心计算坐标
    x = center[0] + math.cos(math.radians(angle_p2p1p3 / 2)) * (radius + text_offset)
    y = center[1] + math.sin(math.radians(angle_p2p1p3 / 2)) * (radius + text_offset)

    # 在弧线上方或下方放置角度的文本
    ax.text(x, y, f"{angle_p2p1p3:.2f}°", fontsize=10, ha="center", va="center", color=color)


def locate_receiver_by_angle(p1, p2, p3, angles):
    angle1, angle2, angle3 = angles
    x = (p1[0]*angle1 + p2[0]*angle2 + p3[0]*angle3) / (angle1 + angle2 + angle3)
    y = (p1[1]*angle1 + p2[1]*angle2 + p3[1]*angle3) / (angle1 + angle2 + angle3)
    return (x, y)

p1 = (0, 0)
radius = 100
p2 = (radius*math.cos(math.radians(0)), radius*math.sin(math.radians(0)))
p3 = (radius*math.cos(math.radians(40)), radius*math.sin(math.radians(40)))
p4 = (radius*math.cos(math.radians(80)), radius*math.sin(math.radians(30))) #被接受信号无人机误差的位置
p0 = (radius*math.cos(math.radians(80)), radius*math.sin(math.radians(80))) #被接受信号无人机误差的位置

print("p2 的坐标:", p2)
print("p3 的坐标:", p3)

receivers_angles = [
    [60, 45, 75],
    [65, 50, 70],
    [70, 55, 65]
]

fig, ax = plt.subplots(figsize=(10, 10))

# 初始化无人机的位置
def init():
    ax.scatter(p1[0], p1[1], color='red', label='FY00 (圆心无人机)')
    ax.scatter(p2[0], p2[1], color='blue', label='发射信号的无人机1')
    ax.scatter(p3[0], p3[1], color='blue', label='发射信号的无人机2')
    ax.scatter(p4[0], p4[1], color='black', label='被迫接受信号无人机')

    for i in range(2, 9):
        px = radius*math.cos(math.radians(40*i))
        py = radius*math.sin(math.radians(40*i))
        ax.scatter(px, py, color='green')
    ax.set_xlim(-120, 120)
    ax.set_ylim(-120, 120)
    ax.set_title('无人机的位置示意图')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True)
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.legend()
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='grey')# 连接p1, p2
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], color='grey')# 连接p1, p3
    ax.plot([p1[0], p4[0]], [p1[1], p4[1]], color='grey')  # 连接p1, p4
    ax.plot([p3[0], p2[0]], [p3[1], p2[1]], color='grey')  # 连接p1, p4
    ax.plot([p4[0], p3[0]], [p4[1], p3[1]], color='grey')  # 连接p1, p4
    ax.plot([p4[0], p2[0]], [p4[1], p2[1]], color='grey')  # 连接p1, p4

    # 在图上绘制角度
    draw_angle_annotation(ax, p1, p2, p3)
# 更新被动接收信号的无人机的位置
def update(num):
    ax.clear()
    init()
    angles = receivers_angles[num]
    position = locate_receiver_by_angle(p1, p2, p3, angles)
    # ax.scatter(position[0], position[1], color='orange', s=100, label=f'被动接收信号的无人机{num+1}')
    ax.legend()


def compute_angle(p1, p2, p3):
    # 定义向量a和b
    a = (p2[0] - p1[0], p2[1] - p1[1])
    b = (p3[0] - p1[0], p3[1] - p1[1])

    # 计算两个向量的点积
    dot_product = a[0] * b[0] + a[1] * b[1]

    # 计算两个向量的长度
    mag_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
    mag_b = math.sqrt(b[0] ** 2 + b[1] ** 2)

    # 计算夹角的余弦值
    cos_theta = dot_product / (mag_a * mag_b)

    # 计算夹角的弧度值
    theta_rad = math.acos(cos_theta)

    # 将夹角从弧度转换为度
    theta_deg = math.degrees(theta_rad)

    return theta_deg


angle_p2p1p3 = compute_angle(p1, p2, p3)
print(f"角 p2p1p3 的大小为: {angle_p2p1p3:.2f}°")

ani = animation.FuncAnimation(fig, update, frames=len(receivers_angles), repeat=True)
plt.show()


