"""Unit tests for Cliff's delta implementation."""

from __future__ import annotations

import numpy as np

from tasks.t0125_t0123_cluster_factor_mi_atp.code.effect_sizes import cliffs_delta


def test_cliffs_delta_x_all_less() -> None:
    x: np.ndarray = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    y: np.ndarray = np.array([4.0, 5.0, 6.0], dtype=np.float64)
    assert cliffs_delta(x, y) == -1.0


def test_cliffs_delta_x_all_greater() -> None:
    x: np.ndarray = np.array([4.0, 5.0, 6.0], dtype=np.float64)
    y: np.ndarray = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    assert cliffs_delta(x, y) == 1.0


def test_cliffs_delta_identical() -> None:
    x: np.ndarray = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    y: np.ndarray = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    assert cliffs_delta(x, y) == 0.0


def test_cliffs_delta_ties_only() -> None:
    x: np.ndarray = np.array([2.0, 2.0, 2.0], dtype=np.float64)
    y: np.ndarray = np.array([2.0, 2.0, 2.0], dtype=np.float64)
    assert cliffs_delta(x, y) == 0.0


def test_cliffs_delta_partial_overlap() -> None:
    x: np.ndarray = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    y: np.ndarray = np.array([2.0, 3.0], dtype=np.float64)
    # x_i > y_j pairs: (3,2),(4,2),(4,3) = 3; x_i < y_j: (1,2),(1,3),(2,3) = 3 => delta = 0
    assert cliffs_delta(x, y) == 0.0


def test_cliffs_delta_known_negative() -> None:
    # x slightly lower on average than y => negative delta
    x: np.ndarray = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    y: np.ndarray = np.array([3.0, 4.0, 5.0, 6.0], dtype=np.float64)
    # x > y: (4,3) = 1; x < y: (1,3),(1,4),(1,5),(1,6),(2,3),(2,4),(2,5),(2,6),
    #         (3,4),(3,5),(3,6),(4,5),(4,6) = 13; delta = (1-13)/16 = -0.75
    assert cliffs_delta(x, y) == -0.75
