# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
import math
import random
import uuid

import numpy as np
from rtree import index

from src.utilities.geometry import distance_between_points


class ConfigurationSpace(object):
    def __init__(self, dimension_lengths: list, O: list = None):
        """
        Initialize Configuration Space
        :param dimension_lengths: range of each dimension
        :param O: list of obstacles
        """
        # sanity check
        if len(dimension_lengths) < 2:
            raise Exception("Must have at least 2 dimensions")
        self.dimensions = len(dimension_lengths)  # number of dimensions
        # sanity checks
        if any(len(i) != 2 for i in dimension_lengths):
            raise Exception("Dimensions can only have a start and end")
        if any(i[0] >= i[1] for i in dimension_lengths):
            raise Exception("Dimension start must be less than dimension end")
        self.dimension_lengths = dimension_lengths  # length of each dimension
        p = index.Property()
        p.dimension = self.dimensions
        # r-tree representation of obstacles
        # sanity check
        if any(len(o) / 2 != len(dimension_lengths) for o in O):
            raise Exception("Obstacle has incorrect dimension definition")
        if any(o[i] >= o[int(i + len(o) / 2)] for o in O for i in range(int(len(o) / 2))):
            raise Exception("Obstacle start must be less than obstacle end")
        if O is None:
            self.obs = index.Index(interleaved=True, properties=p)
        else:
            self.obs = index.Index(obstacle_generator(O), interleaved=True, properties=p)

    def obstacle_free(self, x: tuple) -> bool:
        """
        Check if a location resides inside of an obstacle
        :param x: location to check
        :return: True if not inside an obstacle, False otherwise
        """
        return self.obs.count(x) == 0

    def sample_free(self) -> tuple:
        """
        Sample a location within X_free
        :return: random location within X_free
        """
        while True:  # sample until not inside of an obstacle
            x = self.sample()
            if self.obstacle_free(x):
                return x

    def collision_free(self, start: tuple, end: tuple, r: float) -> bool:
        """
        Check if a line segment intersects an obstacle
        :param start: starting point of line
        :param end: ending point of line
        :param r: resolution of points to sample along edge when checking for collisions
        :return: True if line segment does not intersect an obstacle, False otherwise
        """
        dist = distance_between_points(start, end)
        j = 2
        already_checked = set()  # points along edge that have already been checked for collisions
        # perform iterative deepening search along edge
        while j <= dist / r:
            safe, already_checked = self.check_along_edge(start, end, j, already_checked)
            if not safe:
                return False

            j *= 2

        # check at maximum user-defined resolution
        if j / 2 != r:
            safe, already_checked = self.check_along_edge(start, end, int(math.ceil(dist / r)), already_checked)
            if not safe:
                return False

        return True

    def check_along_edge(self, start, end, j, already_checked):
        """
        Check points along an edge for collision
        :param start: starting point of line
        :param end: ending point of line
        :param j: number of points to use when discretizing line
        :param already_checked: set of points that have already been queried
        :return: True if line segment does not intersect an obstacle, False otherwise, set of points that were queried
        """
        dim_linspaces = [np.linspace(s_i, e_i, j) for s_i, e_i in zip(start, end)]
        points = set([point for point in zip(*dim_linspaces)])
        points = points - already_checked  # remove points that have already been queried
        already_checked = already_checked | points  # update queried points
        if not all(self.obstacle_free(point) for point in points):
            return False, already_checked

        return True, already_checked

    def sample(self) -> tuple:
        """
        Return a random location within X
        :return: random location within X (not necessarily X_free)
        """
        x = []
        for dimension in range(len(self.dimension_lengths)):
            x.append(random.uniform(self.dimension_lengths[dimension][0], self.dimension_lengths[dimension][1]))

        x = tuple(x)

        return x


def obstacle_generator(obstacles):
    """
    Add obstacles to r-tree
    :param obstacles: list of obstacles
    """
    for obstacle in obstacles:
        yield (uuid.uuid4(), obstacle, obstacle)
