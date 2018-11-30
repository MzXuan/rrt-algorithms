# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import sys
sys.path.insert(0, '/home/xuan/Code/rrt-algorithms')
import numpy as np

from src.rrt.rrt import RRT
from src.search_space.search_space import SearchSpace
from src.utilities.plotting import Plot
import random_map

x_dim=500
y_dim=500
X_dimensions = np.array([(0, x_dim), (0, y_dim)])  # dimensions of Search Space
# obstacles
test = random_map.random_2d_map(x_dim,y_dim)

# Obstacles = np.array([(20, 20, 40, 40), (20, 60, 40, 80), (60, 20, 80, 40), (60, 60, 80, 80)])
Obstacles = test
x_init = (0, 0)  # starting location
x_goal = (x_dim, y_dim)  # goal location

Q = np.array([(2, 40)])  # length of tree edges
r = 0.1  # length of smallest edge to check for intersection with obstacles
max_samples = 9999  # max number of samples to take before timing out
prc = 0.1  # probability of checking for a connection to goal

# create search space
X = SearchSpace(X_dimensions, Obstacles)

# create rrt_search
rrt = RRT(X, Q, x_init, x_goal, max_samples, r, prc)
path = rrt.rrt_search()

# plot
plot = Plot("rrt_2d")
plot.plot_tree(X, rrt.trees)
if path is not None:
    plot.plot_path(X, path)
plot.plot_obstacles(X, Obstacles)
plot.plot_start(X, x_init)
plot.plot_goal(X, x_goal)
plot.draw(auto_open=True)
