# 处理虚线，两点连接变色
# 需要alpha和gramme的角度

import numpy as np
import matplotlib.pyplot as plt

# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建一个3D图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 设定坡度
alpha = np.radians(1.5)
# 区域边长
long = 4000
# 给定beta的值
beta = np.radians(float(input("请输入beta的角度值(例如：30): ")))

# 创建一个海平面
x_plane = np.linspace(0, long, 100)
y_plane = np.linspace(0, long, 100)
x_plane, y_plane = np.meshgrid(x_plane, y_plane)
z_plane = np.zeros_like(x_plane)
ax.plot_surface(x_plane, y_plane, z_plane, alpha=0.5, color='blue')

# 根据坡度和相交点创建一个海底平面
x_seabed = np.linspace(0, long, 100)
y_seabed = np.linspace(0, long, 100)
x_seabed, y_seabed = np.meshgrid(x_seabed, y_seabed)
z_seabed = (x_seabed) * np.tan(alpha)
ax.plot_surface(x_seabed, y_seabed, z_seabed, color='brown', alpha=0.5)

# 计算船的Z坐标
ship_z = 200 * np.tan(alpha) + 120

# 在船的位置绘制一个红色的点
ax.scatter(long/2, long/2, ship_z, c='red', s=100, label='船舶')

# 定义旋转向量的函数
def rotate_vector(vector, angle):
    """旋转一个2D向量给定的角度"""
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    return np.dot(rotation_matrix, vector)

# 由坡度确定的坡面法线的投影
normal_projection = np.array([np.cos(alpha), np.sin(alpha)])
# 绘制坡面法线在xy平面的投影
projection_length = 1000  # 你可以更改投影的长度
ax.quiver(long/2, long/2, 0, normal_projection[0], normal_projection[1], 0, length=projection_length, color='purple', label='坡面法线投影')

# 船舶测线方向的投影
ship_direction_projection = rotate_vector(normal_projection, beta)
# 计算船舶开角的虚线的方向
direction1 = rotate_vector(ship_direction_projection, np.pi/2)
direction2 = rotate_vector(ship_direction_projection, -np.pi/2)

# 绘制船舶测线方向投影
measuring_length = 1000  # 可更改的测量线长度
end_x = long/2 + measuring_length * ship_direction_projection[0]
end_y = long/2 + measuring_length * ship_direction_projection[1]
ax.plot([long/2, end_x], [long/2, end_y], [0, 0], 'g--', linewidth=1.5, label="测线方向投影")

# 绘制船舶开角的虚线
max_dist = ship_z / np.sin(beta)
for direction in [direction1, direction2]:
    end_x = long/2 + max_dist * direction[0]
    end_y = long/2 + max_dist * direction[1]
    ax.plot([long/2, end_x], [long/2, end_y], [ship_z, 0], 'r--', linewidth=1.5)

# 添加β角度标注
angle_annotation_pos = (long/2 + 0.5 * projection_length * (normal_projection[0] + ship_direction_projection[0]),
                        long/2 + 0.5 * projection_length * (normal_projection[1] + ship_direction_projection[1]))
ax.text(angle_annotation_pos[0], angle_annotation_pos[1], 0, f'β = {np.degrees(beta):.2f}°', color='black')

# 固定坐标轴的范围以及坐标轴信息
ax.set_zlim(0, 200)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D 视图')
ax.legend()

# 显示图
plt.show()
