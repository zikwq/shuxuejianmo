import math
# 用户输入beta和d的角度值然后通过方法转化为弧度值
beta = math.radians(float(input("请输入 bate 的角度值: ")))
# beta = math.radians(0)
d = 3889.2


D0=120
D = (D0+d*math.tan(math.radians(1.5))*math.cos(beta))
alpha = math.acos(math.sqrt(math.cos(math.radians(1.5))**2 * math.sin(beta)**2 + math.cos(beta)**2))
w = (math.sin(math.radians(60))/math.sin(math.radians(30)+alpha)+math.sin(math.radians(60))/math.sin(math.radians(30)-alpha))*D*math.cos(alpha)
# 结果保留一位小数
w_rounded = round(w, 1)
print(w_rounded)
print(alpha)
print(D)
