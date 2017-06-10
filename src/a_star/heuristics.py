# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

from src.utilities.geometry import distance_between_points


def heuristic(a: tuple, b: tuple) -> float:
    """
    Heuristic used for A*
    :param a: current location
    :param b: next location
    :return: estimated cost-to-go from a to b
    """
    return distance_between_points(a, b)
