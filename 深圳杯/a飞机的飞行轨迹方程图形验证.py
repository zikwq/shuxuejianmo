import numpy as np
import matplotlib.pyplot as plt

# 1. Extra Circular Motion
theta = np.linspace(0, 2*np.pi, 100)
x1 = 1.3 + 0.3 * np.cos(theta)
y1 = 0.3 * np.sin(theta)

# 2. New Line from Circle End to Tangent using the provided equation
x2 = np.linspace(1, 0.25, 100)
y2 = 0.4330127018922193 * (x2 - 1) / (0.25 - 1)

# 3. Circle around Obstacle
r = 0.5  # sqrt(0.25)
x3 = r * np.cos(theta)
y3 = r * np.sin(theta)

# 4. Line from Tangent to B
x4 = np.linspace(-0.07142857142857142, -3.5, 100)
y4 = (x4 + 0.07142857142857142) * (0.0 - 0.4948716593053935) / (-3.5 + 0.07142857142857142) + 0.4948716593053935

plt.figure(figsize=(10, 8))

plt.plot(x1, y1, label="Extra Circular Motion")
plt.plot(x2, y2, label="Line from Circle End to Tangent")
plt.plot(x3, y3, label="Circle around Obstacle")
plt.plot(x4, y4, label="Line from Tangent to B")

plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Trajectory of a drone')
plt.legend()
plt.grid(True)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.show()
