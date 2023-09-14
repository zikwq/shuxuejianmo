import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 三架发射无人机的位置
A = (0, 0)
B = (5, 0)
C = (2.5, 4.33)  # 使用等边三角形的形状来表示位置

# 目标无人机的位置
T = (3, 2)

fig, ax = plt.subplots(figsize=(10, 8))

# 初始化函数：只绘制基本的点
def init():
    ax.scatter(*A, s=100, color='r', label='A')
    ax.scatter(*B, s=100, color='g', label='B')
    ax.scatter(*C, s=100, color='b', label='C')
    ax.scatter(*T, s=100, color='y', label='T')
    ax.set_xlim(-2, 7)
    ax.set_ylim(-2, 7)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("动态显示角度")
    ax.grid(True)
    ax.legend(loc="upper right")
    return fig,

# 更新函数：为动画的每一帧绘制新的元素
def update(frame):
    if frame == 1:  # 连接A和T
        ax.plot([A[0], T[0]], [A[1], T[1]], 'r--')
    elif frame == 2:  # 显示角度A
        angleA = np.degrees(np.arctan2(T[1]-A[1], T[0]-A[0]))
        arcA = patches.Arc(A, 1.5, 1.5, angle=0, theta1=0, theta2=angleA, color='r')
        ax.add_patch(arcA)
    elif frame == 3:  # 连接B和T
        ax.plot([B[0], T[0]], [B[1], T[1]], 'g--')
    elif frame == 4:  # 显示角度B
        angleB = np.degrees(np.arctan2(T[1]-B[1], T[0]-B[0]))
        if angleB < 0:
            angleB += 360
        arcB = patches.Arc(B, 1.5, 1.5, angle=0, theta1=0, theta2=angleB, color='g')
        ax.add_patch(arcB)
    elif frame == 5:  # 连接C和T
        ax.plot([C[0], T[0]], [C[1], T[1]], 'b--')
    elif frame == 6:  # 显示角度C
        angleC = np.degrees(np.arctan2(T[1]-C[1], T[0]-C[0]))
        if angleC < 0:
            angleC += 360
        arcC = patches.Arc(C, 1.5, 1.5, angle=0, theta1=0, theta2=angleC, color='b')
        ax.add_patch(arcC)
    return fig,

ani = FuncAnimation(fig, update, frames=range(7), init_func=init, blit=False)
plt.show()
