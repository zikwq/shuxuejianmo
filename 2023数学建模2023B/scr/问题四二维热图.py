import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the provided Excel file
data = pd.read_excel("../data/附件.xlsx", header=None)

# Extracting the coordinates information from the original data
x_coords_new = data.iloc[1, 2:].values.astype(float)
y_coords_new = data.iloc[2:, 1].values.astype(float)

# Cleaning the data
cleaned_data_new = data.iloc[2:, 2:].apply(pd.to_numeric, errors='coerce')

# Define the aspect ratio based on the actual region dimensions
aspect_ratio_new = 5 / 4  # South-North length (5 NM) divided by West-East width (4 NM)
cmap_inverted_new = plt.get_cmap("terrain").reversed()

# Generate meshgrid based on x_coords and y_coords
X_new, Y_new = np.meshgrid(x_coords_new, y_coords_new)

# Plotting the cleaned data using the generated meshgrid
plt.figure(figsize=(8, 10))
ax = plt.gca()
ax.set_aspect(aspect_ratio_new)

plt.pcolormesh(X_new, Y_new, cleaned_data_new.values, cmap=cmap_inverted_new, shading='auto')
plt.colorbar(label="Depth (m)")
plt.title("Seabed Depth Profile")
plt.xlabel("Distance (nautical miles) - West to East")
plt.ylabel("Distance (nautical miles) - South to North")

plt.show()
