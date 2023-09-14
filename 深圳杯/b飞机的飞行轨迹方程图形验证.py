# b飞机的飞行轨迹
# 1. Line from B to Tangent: y = -0.14433756729740646x + -0.5051814855409226
# 2. Circle around Obstacle: (x - 0)^2 + (y - 0)^2 = 0.25
# 3. Line from Tangent to A: y = 0.5773502691896251x + -0.5773502691896251

import numpy as np
import matplotlib.pyplot as plt

# 1. Line from B to Tangent
x1 = np.linspace(-3.5, 0, 100)  # Let's take a range from -3.5 to 0 for visualization
y1 = -0.14433756729740646 * x1 - 0.5051814855409226

# 2. Circle around Obstacle
theta = np.linspace(0, 2*np.pi, 100)
r = 0.5  # sqrt(0.25)
x2 = r * np.cos(theta)
y2 = r * np.sin(theta)

# 3. Line from Tangent to A
x3 = np.linspace(0, 1, 100)  # Let's take a range from 0 to 1 for visualization
y3 = 0.5773502691896251 * x3 - 0.5773502691896251

plt.figure(figsize=(10, 8))

plt.plot(x1, y1, label="Line from B to Tangent")
plt.plot(x2, y2, label="Circle around Obstacle")
plt.plot(x3, y3, label="Line from Tangent to A")

plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Trajectory of a drone')
plt.legend()
plt.grid(True)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.show()
