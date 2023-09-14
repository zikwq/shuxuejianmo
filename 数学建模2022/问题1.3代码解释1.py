import numpy as np
import matplotlib.pyplot as plt

# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义发射无人机和被动接收无人机的位置
signal_drone_position = (100, 0)
passive_drone_position = (80, 30)

# 计算角度
angle = np.arctan2(passive_drone_position[0] * np.sin(np.radians(passive_drone_position[1])) - signal_drone_position[0] * np.sin(np.radians(signal_drone_position[1])),
                   passive_drone_position[0] * np.cos(np.radians(passive_drone_position[1])) - signal_drone_position[0] * np.cos(np.radians(signal_drone_position[1])))

# 转换角度为度数
angle_degrees = np.degrees(angle)

# 绘制图像
plt.figure(figsize=(6, 6))
plt.polar(np.radians(signal_drone_position[1]), signal_drone_position[0], 'ro', label='发射无人机')
plt.polar(np.radians(passive_drone_position[1]), passive_drone_position[0], 'bo', label='被动接收无人机')
plt.polar([np.radians(signal_drone_position[1]), np.radians(passive_drone_position[1])], [signal_drone_position[0], passive_drone_position[0]], 'g-', label='夹角')
plt.legend()
plt.title("无人机位置和夹角关系")
plt.show()
