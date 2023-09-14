#####根据用户输入角度，计算被接受信号的无人机具体坐标#####
import random
import math

# 1. 定义半径和随机获取的待测点
r = 10  # 定义一个半径限制随机选择的范围（根据您的需要调整）
px_x_real = random.uniform(1, 3)
px_y_real = random.uniform(8, 11)

# 2. 获取alpha_1和alpha_2的角度值
import numpy as np

def calculate_angle(A, B, C):
    # 计算向量
    BA = np.array([A[0]-B[0], A[1]-B[1]])
    BC = np.array([C[0]-B[0], C[1]-B[1]])

    # 计算两向量之间的夹角
    cos_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))  # 这里使用clip是为了防止计算误差导致cos_angle稍微超过[-1, 1]的范围

    return angle

#定义点坐标，p1,p2,p3,p4
p1 = (0, 0)
p2 = (r*math.cos(math.radians(0)), r*math.sin(math.radians(0)))
p3 = (r*math.cos(math.radians(40)), r*math.sin(math.radians(40)))
p4_real = (px_x_real, px_y_real)
#获取角度值
alpha_1 = calculate_angle(p1,p4_real, p2)
alpha_2 = calculate_angle(p3,p4_real, p2)
alpha_3 = alpha_1 + alpha_2

# 由于使用math库，我们需要采用数值方法求解方程
# 为此，我们可以定义一个函数，表示我们的方程系统，并使用数值方法求其零点

def equations(vars):
    x, beta = vars
    eq1 = r / math.sin(alpha_1) - x / math.sin(math.radians(140) - alpha_1 - beta)
    eq2 = r / math.sin(alpha_3) - x / math.sin(math.radians(180) - alpha_3 - beta)
    return [eq1, eq2]

# 使用scipy.optimize的fsolve函数求解非线性方程组
from scipy.optimize import fsolve

# 为x和beta提供一个初始猜测值
initial_guess = [r, 100]  # 这只是一个示例初始猜测值，可能需要调整
x_val, beta_val = fsolve(equations, initial_guess)
beta_val = math.degrees(beta_val)+40   #beta最终的角度值

beta_val_rad = math.radians(beta_val)  # 将beta_val转换回弧度形式进行计算x,y坐标
px_x = x_val * math.cos(beta_val_rad) #计算x,y的坐标
px_y = x_val * math.sin(beta_val_rad) #计算x,y的坐标
# 打印解决方案
print("计算得到的被接收信息无人机坐标为 =", px_x,px_y)

print("待测点p4的真实坐标:            ", px_x_real, px_y_real)


####开始绘画图像#####

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
p1 = (0, 0)
p2 = (r*math.cos(math.radians(0)), r*math.sin(math.radians(0)))
p3 = (r*math.cos(math.radians(40)), r*math.sin(math.radians(40)))
p4 = (px_x, px_y) #被接受信号无人机误差的位置
p0 = (r*math.cos(math.radians(80)), r*math.sin(math.radians(80))) #被接受信号无人机圆周上的位置


fig, ax = plt.subplots(figsize=(10, 10))




# 初始化无人机的位置
def init():
    ax.scatter(p1[0], p1[1], color='red', label='FY00 (圆心无人机)')
    ax.scatter(p2[0], p2[1], color='blue', label='发射信号的无人机1')
    ax.scatter(p3[0], p3[1], color='blue', label='发射信号的无人机2')
    ax.scatter(p4[0], p4[1], color='black', label='被迫接受信号无人机')
    ax.scatter(px_x_real, px_y_real, color='red', label='随机生成无人机位置')



    for i in range(2, 9):
        px = r*math.cos(math.radians(40*i))
        py = r*math.sin(math.radians(40*i))
        ax.scatter(px, py, color='green')
    ax.set_xlim(-r-r*0.2, r+r*0.2)
    ax.set_ylim(-r-r*0.2, r+r*0.2)
    ax.set_title('无人机的位置问题1.1解题示意图')
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


def update(num):
    ax.clear()
    init()
    ax.legend()


ani = animation.FuncAnimation(fig, update, repeat=True)
plt.show()


