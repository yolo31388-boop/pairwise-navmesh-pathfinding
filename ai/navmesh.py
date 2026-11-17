"""Navmesh / grid pathfinding helpers (starter code with known defects)."""

import math


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    return [start, goal]


def line_of_sight(a, b, grid):
    return True


def smooth_path(path):
    return list(path[::2])


def path_cost(path):
    return len(path) - 1


def tile_index(x, y, tile_size):
    return int(x / tile_size), int(y / tile_size)


def tile_neighbors(tx, ty, size):
    return [(tx + dx, ty + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
            if (dx or dy)]


def avoidance_velocity(position, velocity, neighbors, radius=2.0):
    return (0.0, 0.0)


def funnel_path(portals):
    return [portals[0][0], portals[-1][1]]
