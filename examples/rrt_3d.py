# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import sys

sys.path.insert(0, '/home/xuan/Code/rrt-algorithms')

import numpy as np

from src.rrt.rrt import RRT
from src.search_space.search_space import SearchSpace
from src.utilities.plotting import Plot
import random_map

x_dim=100
y_dim=100
z_dim=100

X_dimensions = np.array([(0, x_dim), (0, y_dim), (0, z_dim)])  # dimensions of Search Space

# obstacles
test = random_map.random_3d_map(x_dim,y_dim,z_dim)
Obstacles = test
# obstacles
# Obstacles = np.array(
#     [(20, 20, 20, 40, 40, 40), (20, 20, 60, 40, 40, 80), (20, 60, 20, 40, 80, 40), (60, 60, 20, 80, 80, 40),
#      (60, 20, 20, 80, 40, 40), (60, 20, 60, 80, 40, 80), (20, 60, 60, 40, 80, 80), (60, 60, 60, 80, 80, 80)])
x_init = (0, 0, 0)  # starting location
x_goal = (x_dim, y_dim, z_dim)  # goal location

Q = np.array([(8, 4)])  # length of tree edges
Q = np.array([(8, 4)])  # length of tree edges
r = 1  # length of smallest edge to check for intersection with obstacles
max_samples = 1024  # max number of samples to take before timing out
prc = 0.1  # probability of checking for a connection to goal

# create Search Space
X = SearchSpace(X_dimensions, Obstacles)

# create rrt_search
rrt = RRT(X, Q, x_init, x_goal, max_samples, r, prc)
path = rrt.rrt_search()

# plot
plot = Plot("rrt_3d")
plot.plot_tree(X, rrt.trees)
if path is not None:
    plot.plot_path(X, path)
plot.plot_obstacles(X, Obstacles)
plot.plot_start(X, x_init)
plot.plot_goal(X, x_goal)
plot.draw(auto_open=True)
