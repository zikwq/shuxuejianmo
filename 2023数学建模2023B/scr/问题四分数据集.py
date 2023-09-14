import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import random
import math

# 1. 加载数据
data = pd.read_excel("../data/附件.xlsx", header=None)
x_coords = data.iloc[1, 2:].values.astype(float)
y_coords = data.iloc[2:, 1].values.astype(float)
depth_data = data.iloc[2:, 2:].apply(pd.to_numeric, errors='coerce')

# 2. 定义常量和参数
METERS_IN_ONE_NAUTICAL_MILE = 1852
LENGTH = 5 * METERS_IN_ONE_NAUTICAL_MILE
WIDTH = 4 * METERS_IN_ONE_NAUTICAL_MILE

def seabedCoverage(individual):
    total_length = 0
    uncovered_area = 0
    overlapped_area = 0
    covered_areas = []

    for i in range(0, len(individual), 4):
        x1, y1 = individual[i], individual[i + 1]
        x2, y2 = individual[i + 2], individual[i + 3]
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        total_length += length

        # Calculate the areas covered by the sensors using the coordinates of the rectangle
        rect = [(x1, y1), (x2, y2), (x2 + WIDTH, y2), (x1 + WIDTH, y1)]
        covered_areas.append(rect)

    for i in range(len(covered_areas)):
        for j in range(i+1, len(covered_areas)):
            overlap = get_overlap(covered_areas[i], covered_areas[j])
            overlapped_area += overlap

    total_area = (max(x_coords) - min(x_coords)) * (max(y_coords) - min(y_coords))
    total_covered_area = len(covered_areas) * LENGTH * WIDTH
    uncovered_area = total_area - total_covered_area + overlapped_area

    fitness_value = total_length + 10 * uncovered_area + 5 * overlapped_area
    return fitness_value,

def get_overlap(rect1, rect2):
    dx = min(rect1[1][0], rect2[1][0]) - max(rect1[0][0], rect2[0][0])
    dy = min(rect1[1][1], rect2[1][1]) - max(rect1[0][1], rect2[0][1])
    if (dx >= 0) and (dy >= 0):
        return dx * dy
    return 0

# Genetic Algorithm Initialization
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float_x", random.uniform, min(x_coords), max(x_coords))
toolbox.register("attr_float_y", random.uniform, min(y_coords), max(y_coords))
toolbox.register("individualCreator", tools.initCycle, creator.Individual, (toolbox.attr_float_x, toolbox.attr_float_y, toolbox.attr_float_x, toolbox.attr_float_y), n=5)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

toolbox.register("evaluate", seabedCoverage)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxBlend, alpha=0.1)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=1.0, low=min(x_coords), up=max(x_coords), indpb=0.2)

# Genetic Algorithm Execution
POPULATION_SIZE = 50
P_CROSSOVER = 0.7
P_MUTATION = 0.2
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 5

population = toolbox.populationCreator(n=POPULATION_SIZE)
hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("min", np.min)
stats.register("max", np.max)

population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION, ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

# Visualization
X, Y = np.meshgrid(x_coords, y_coords)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Adjust depth data to be negative for visualization
adjusted_depth_data = -depth_data.values

# Plot seabed
surf = ax.plot_surface(X, Y, adjusted_depth_data, cmap="viridis")

# Plot individual solutions
for individual in hof:
    for i in range(0, len(individual), 4):
        x1, y1 = individual[i], individual[i + 1]
        x2, y2 = individual[i + 2], individual[i + 3]
        ax.plot([x1, x2], [y1, y2], zs=[-max(adjusted_depth_data.flatten()), -max(adjusted_depth_data.flatten())], color="r")

plt.show()
