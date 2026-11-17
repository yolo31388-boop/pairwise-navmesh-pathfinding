import pytest

from ai.navmesh import (astar, avoidance_velocity, heuristic, line_of_sight,
                        path_cost, smooth_path, tile_index, tile_neighbors)

DIAG = 2 ** 0.5


def test_heuristic_octile_for_diagonal():
    assert heuristic((0, 0), (3, 3)) == pytest.approx(3 * DIAG)


def test_heuristic_octile_for_mixed_axis():
    assert heuristic((0, 0), (3, 1)) == pytest.approx(2 + DIAG)


def test_astar_routes_around_wall():
    grid = ["...", ".#.", "..."]
    path = astar(grid, (0, 0), (2, 2))
    assert path_cost(path) == pytest.approx(4.0)


def test_astar_returns_none_when_goal_is_blocked():
    grid = [".#.", ".#.", "..."]
    assert astar(grid, (0, 0), (1, 0)) is None


def test_astar_forbids_diagonal_corner_cutting():
    grid = [".#.", "..."]
    path = astar(grid, (0, 0), (1, 1))
    assert path_cost(path) == pytest.approx(2.0)


def test_astar_rejects_out_of_bounds_goal():
    grid = ["...", "...", "..."]
    assert astar(grid, (0, 0), (5, 5)) is None


def test_line_of_sight_detects_blocking_wall():
    grid = ["...", ".#.", "..."]
    assert line_of_sight((0, 0), (2, 2), grid) is False
    assert line_of_sight((0, 0), (2, 1), grid) is True


def test_smooth_path_removes_collinear_points():
    path = [(0, 0), (1, 0), (2, 0), (2, 1)]
    assert smooth_path(path) == [(0, 0), (2, 0), (2, 1)]


def test_smooth_path_keeps_corners():
    path = [(0, 0), (1, 0), (1, 1), (2, 1)]
    assert smooth_path(path) == path


def test_path_cost_sums_euclidean_lengths():
    assert path_cost([(0, 0), (3, 4)]) == pytest.approx(5.0)


def test_tile_index_floors_negative_coordinates():
    assert tile_index(-0.5, 3.2, 4) == (-1, 0)


def test_tile_neighbors_for_corner_tile():
    assert tile_neighbors(0, 0, 2) == [(1, 0), (0, 1)]


def test_tile_neighbors_for_interior_tile():
    assert len(tile_neighbors(1, 1, 3)) == 4


def test_avoidance_pushes_away_from_close_neighbor():
    push = avoidance_velocity((0.0, 0.0), (1.0, 0.0), [(1.0, 0.0)], radius=2.0)
    assert push[0] < 0
    assert abs(push[0]) > 0


def test_avoidance_sums_neighbors_on_the_same_side():
    push = avoidance_velocity((0.0, 0.0), (1.0, 0.0),
                              [(1.0, 0.0), (1.0, 1.0)], radius=2.0)
    assert push[0] < 0
    assert push[1] < 0


