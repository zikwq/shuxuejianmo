import pandas as pd
import math
import matplotlib.pyplot as plt

# Let's start by reloading the data to ensure we have the correct depth information.
depth_data_frame = pd.read_excel("../data/附件剪切2.xlsx", header=None)

# Extracting the depth information
depth_data = depth_data_frame.values[1:, 1:].astype(float)

# Extracting the coordinates
x_coords = depth_data_frame.values[0, 1:].astype(float) * 1852  # Convert from nautical miles to meters
y_coords = depth_data_frame.values[1:, 0].astype(float) * 1852  # Convert from nautical miles to meters

# For verification purposes, let's calculate the coverage width for a few depth values from the dataset
def coverage_width(depth):
    return 2 * math.tan(math.radians(60)) * depth

# Picking some random depth values from the data for verification
sample_depths = [depth_data[10][10], depth_data[20][20], depth_data[30][30]]
sample_coverages = [coverage_width(d) for d in sample_depths]

print(sample_depths, sample_coverages)
import pandas as pd
import numpy as np
from math import tan, radians

# Load the depth data from the provided Excel file
data = pd.read_excel('../data/附件剪切2.xlsx', header=None)

# Define constants
mi_to_m = 1852  # Conversion factor from nautical miles to meters


# Define a function to calculate scan width adjusted for grid size
def adjusted_scan_width(depth):
    # Calculate scan width in meters
    width_m = 2 * tan(radians(60)) * depth

    # Convert width from meters to nautical miles, adjusted for grid size
    width_nmi = width_m / mi_to_m

    # Return the scan width in terms of grid cells
    return width_nmi / grid_width


# Define a function to calculate the distance between two points in grid cells
def distance_between_points(point1, point2):
    delta_lat = (point2[0] - point1[0]) * grid_height
    delta_lon = (point2[1] - point1[1]) * grid_width
    return (delta_lat ** 2 + delta_lon ** 2) ** 0.5


# Define a function to calculate the area covered by a survey line between two points
def covered_area_by_line(point1, point2):
    depth = data.iloc[point1[0], point1[1]]
    width_in_grids = int(adjusted_scan_width(depth) / grid_width)
    length = distance_between_points(point1, point2)

    # Calculate the area covered by the line
    return width_in_grids * length * grid_area


# Define a function to calculate the overlap length of a survey line between two points
def overlap_length(point1, point2):
    depth = data.iloc[point1[0], point1[1]]
    width_in_grids = int(adjusted_scan_width(depth) / grid_width)
    length = distance_between_points(point1, point2)

    # Calculate the overlap for the segment
    overlap = 0
    if point1[1] < point2[1]:  # Moving right
        for j in range(point1[1], point2[1] + 1):
            overlap += np.sum(coverage_matrix[max(0, point1[0] - width_in_grids):point1[0] + 1, j])
    else:  # Moving left
        for j in range(point2[1], point1[1] + 1):
            overlap += np.sum(coverage_matrix[max(0, point1[0] - width_in_grids):point1[0] + 1, j])

    # Only consider overlaps that are more than 20% of the width
    if overlap > 0.2 * width_in_grids:
        return (overlap - 0.2 * width_in_grids) * length
    else:
        return 0


# Load the data and calculate grid dimensions
data_cleaned = data.iloc[1:, 1:].copy()
total_area = 4 * 5  # Total area in square nautical miles
grid_width = 4 / data_cleaned.shape[1]  # East-West dimension in nautical miles
grid_height = 5 / data_cleaned.shape[0]  # North-South dimension in nautical miles
grid_area = grid_width * grid_height  # Area covered by one grid cell in square nautical miles

# Create a matrix to keep track of which areas have been covered
coverage_matrix = np.zeros(data_cleaned.shape)


# Define a function to generate a greedy path with dense coverage
def adjusted_greedy_path_with_dense_coverage():
    path_adjusted_greedy = [(0, 0)]
    current_lat_idx = 0
    current_lon_idx = 0
    right_boundary = len(data_cleaned.columns) - 1
    move_right = True  # Initial direction is right

    while current_lat_idx < len(data_cleaned) - 1:
        # Move either to the right or left boundary based on the current direction
        current_lon_idx = right_boundary if move_right else 0
        path_adjusted_greedy.append((current_lat_idx, current_lon_idx))

        # Determine the next latitude position based on the boundary's depth
        boundary_depth = data_cleaned.iloc[current_lat_idx, current_lon_idx]
        current_width_grid = adjusted_scan_width(boundary_depth)

        # Aim for a denser overlap of about 5%
        ideal_move_distance_grid = 0.95 * current_width_grid
        current_lat_idx += int(ideal_move_distance_grid)

        # Ensure the latitude index is within bounds
        current_lat_idx = min(current_lat_idx, len(data_cleaned) - 1)

        # Switch the move direction for the next iteration
        move_right = not move_right

    return path_adjusted_greedy


# Calculate the total length of the survey line
def calculate_total_length(path):
    total_length = sum(distance_between_points(path[i], path[i + 1])
                       for i in range(len(path) - 1))
    return total_length


# Calculate the missed area percentage
def calculate_missed_area_percentage(path):
    total_covered_area = sum(covered_area_by_line(path[i], path[i + 1])
                             for i in range(len(path) - 1))
    missed_area = total_area - total_covered_area
    missed_area_percentage = (missed_area / total_area) * 100
    return missed_area_percentage


# Calculate the total overlap length exceeding 20%
def calculate_total_overlap_length(path):
    total_overlap_length = sum(overlap_length(path[i], path[i + 1])
                               for i in range(len(path) - 1))
    return total_overlap_length


# Generate the adjusted greedy path with dense coverage
path_adjusted_greedy = adjusted_greedy_path_with_dense_coverage()

# Calculate the required metrics
total_length = calculate_total_length(path_adjusted_greedy)
missed_area_percentage = calculate_missed_area_percentage(path_adjusted_greedy)
total_overlap_length = calculate_total_overlap_length(path_adjusted_greedy)
# Plot the depth distribution with the adjusted dense greedy survey line
plt.figure(figsize=(12, 10))
plt.imshow(data_cleaned.values, cmap='viridis', origin='lower')
plt.colorbar(label='Depth (m)')

# Plotting the adjusted dense greedy survey line
lat_values_adjusted_greedy, lon_values_adjusted_greedy = zip(*path_adjusted_greedy)
plt.plot(lon_values_adjusted_greedy, lat_values_adjusted_greedy, color='red', linestyle='-', linewidth=1, marker='o')

plt.title('Depth Distribution with Adjusted Dense Greedy Survey Line')
plt.xlabel('Longitude Grid Points')
plt.ylabel('Latitude Grid Points')
# Display the results
print("测线的总长度：约为 {:.2f} 海里".format(total_length))
print("漏测海区占总待测海域面积的百分比：约为 {:.2f}%".format(missed_area_percentage))
print("在重叠区域中，重叠率超过 20% 的部分的总长度：约为 {:.2f} 海里".format(total_overlap_length))
plt.show()

#求解平均深度
import pandas as pd

# Load the depth data from the provided Excel file
data = pd.read_excel('../data/附件剪切2.xlsx', header=None)

# Remove the first row and first column (if needed)
data_cleaned = data.iloc[1:, 1:].copy()

# Calculate the average depth
average_depth = data_cleaned.values.mean()

print("海域的平均深度为 {:.2f} 米".format(average_depth))
