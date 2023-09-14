import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reload the data from the provided Excel file
data_new = pd.read_excel("../data/附件剪切2.xlsx", header=None)

# Extracting the coordinates information
x_coords_new = data_new.iloc[1, 2:].values.astype(float)
y_coords_new = data_new.iloc[2:, 1].values.astype(float)
cleaned_data_new = data_new.iloc[2:, 2:].apply(pd.to_numeric, errors='coerce')

# Generate meshgrid based on x_coords and y_coords
X_new, Y_new = np.meshgrid(x_coords_new, y_coords_new)

# Adjusting the 3D visualization
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X_new, Y_new, -cleaned_data_new.values, cmap='terrain', linewidth=0, antialiased=True)

# Adding color bar which maps values to colors
fig.colorbar(surf, ax=ax, pad=0.1, label="Depth (m)")

# Setting labels and title
ax.set_xlabel("West to East (NM)")
ax.set_ylabel("South to North (NM)")
ax.set_zlabel("Depth (m)")
ax.set_title("3D Visualization of Seabed Depth (Adjusted)")

# Rotate the view for better visualization
ax.view_init(elev=30, azim=-60)
# 1. Determine the depths at the four corners
corner_depths = [
    cleaned_data_new.iloc[0, 0],    # Top-left corner
    cleaned_data_new.iloc[0, -1],   # Top-right corner
    cleaned_data_new.iloc[-1, 0],   # Bottom-left corner
    cleaned_data_new.iloc[-1, -1]   # Bottom-right corner
]

# 2. Identify the two shallowest corners
shallowest_indices = np.argsort(corner_depths)[:2]

# Create a dictionary to map index to coordinates
corner_coords = {
    0: (x_coords_new[0], y_coords_new[0]),
    1: (x_coords_new[-1], y_coords_new[0]),
    2: (x_coords_new[0], y_coords_new[-1]),
    3: (x_coords_new[-1], y_coords_new[-1])
}
for idx in range(4):  # For all corners
    if idx not in shallowest_indices:  # If the corner is not one of the shallowest
        for shallow_idx in shallowest_indices:  # Connect it to both shallowest corners
            start_coord = corner_coords[shallow_idx]
            end_coord = corner_coords[idx]
            ax.plot([start_coord[0], end_coord[0]], [start_coord[1], end_coord[1]],
                    [-corner_depths[shallow_idx], -corner_depths[idx]], color='red', linewidth=2)

# Extract coordinates for the two shallowest corners
start_coord = corner_coords[shallowest_indices[0]]
end_coord = corner_coords[shallowest_indices[1]]

# 3. Plot a line between these two corners in the 3D view
ax.plot([start_coord[0], end_coord[0]], [start_coord[1], end_coord[1]], [-corner_depths[shallowest_indices[0]], -corner_depths[shallowest_indices[1]]], color='red', linewidth=2)

# Display the plot
plt.show()


