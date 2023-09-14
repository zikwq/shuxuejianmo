import math


def compute_w(D):
    alpha = math.radians(1.5)

    w = (math.sin(math.radians(60)) / math.sin(math.radians(30) + alpha) + (math.sin(math.radians(60)) / math.sin(math.radians(30) - alpha))) * D * math.cos(alpha)

    return round(w, 1)


D_values = [90.9, 85.7, 80.5, 75.2, 70, 64.8, 59.5, 54.3, 49.1]

for D in D_values:
    print(f"当 D = {D} 时, w = {compute_w(D)} 米")
