import matplotlib.pyplot as plt
import numpy as np

# 圆心坐标
x1, y1 = 0, 0
x2, y2 = 1.3, 0

# 半径
r1, r2 = 0.5, 0.3

# # 绘制两个圆
# theta = np.linspace(0, 2 * np.pi, 100)
# plt.plot(x1 + r1 * np.cos(theta), y1 + r1 * np.sin(theta), 'b')
# plt.plot(x2 + r2 * np.cos(theta), y2 + r2 * np.sin(theta), 'r')

# 计算两个圆心之间的距离
d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# 外公切线交点与两圆心连线之间的夹角
alpha = np.arctan2((r2 - r1), d)

# 外公切线与两圆心连线的夹角
theta = np.pi/2 - alpha

# 计算两条外公切线的端点
x5, y5 = x1 - r1*np.sin(alpha), y1 + r1*np.cos(alpha)
x6, y6 = x2 - r2*np.sin(alpha), y2 + r2*np.cos(alpha)

plt.plot([x5, x6], [y5, y6], 'g-')

# 显示图形
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
