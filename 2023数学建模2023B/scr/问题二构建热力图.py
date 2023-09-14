import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# Data
data = {
    '0': [415.7, 416.1, 416.5, 416.1, 415.7, 416.1, 416.5, 416.1],
    '0.3': [466.1, 451.8, 416.5, 380.4, 365.3, 380.4, 416.5, 451.8],
    '0.6': [516.5, 487.5, 416.5, 344.8, 314.9, 344.8, 416.5, 487.5],
    '0.9': [566.9, 523.1, 416.5, 309.1, 264.5, 309.1, 416.5, 523.1],
    '1.2': [617.3, 558.8, 416.5, 273.4, 214.1, 273.4, 416.5, 558.8],
    '1.5': [667.7, 594.5, 416.5, 237.7, 163.7, 237.7, 416.5, 594.5],
    '1.8': [718.1, 630.2, 416.5, 202.1, 113.3, 202.1, 416.5, 630.2],
    '2.1': [768.5, 665.8, 416.5, 166.4, 62.9, 166.4, 416.5, 665.8]
}

# Convert data to a DataFrame
df = pd.DataFrame(data)

# Set the row names (beta values)
df.index = [0, 45, 90, 135, 180, 225, 270, 315]

# Plotting heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df, annot=True, cmap='coolwarm', fmt=".1f", linewidths=0.5)
plt.title("测线船舶的覆盖宽度")
plt.xlabel("测线船舶与中心点的距离 d(海里)")
plt.ylabel("测线方向夹角 Beta (°)")
plt.show()
