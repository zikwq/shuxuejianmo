import math


def compute_w(beta_degrees, D0=120, d=3889.2, theta_degrees=120, alpha_degrees=1.5):
    beta = math.radians(beta_degrees)
    theta = math.radians(theta_degrees)
    alpha = math.radians(alpha_degrees)

    w = 2 * (D0 + d * math.tan(alpha) * math.cos(beta)) * math.tan(theta / 2)
    return round(w, 1)


beta_values = [0, 45, 90, 135, 180, 225, 270, 315]

for beta in beta_values:
    print(f"当 beta = {beta}° 时, w = {compute_w(beta)}")
