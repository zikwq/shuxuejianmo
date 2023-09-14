import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('data\问题一剪切版本.xlsx')


# 将 DataFrame 保存为 CSV 文件
df.to_csv('问题一剪切版.csv', index=False)
