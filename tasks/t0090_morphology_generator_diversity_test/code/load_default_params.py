"""Load the t0083 best-cell 54-d ParameterVector for use in verification simulation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    N_PARAMS,
    ParameterVector,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    T0083_PARETO_FRONT_JSON,
)


def load_t0083_pareto_cells(*, path: Path = T0083_PARETO_FRONT_JSON) -> list[dict[str, Any]]:
    """Return the list of t0083 Pareto cell records (each has cell_index, params, dsi, ...)."""
    data = json.loads(path.read_text())
    cells = data["cells"]
    assert isinstance(cells, list), f"expected a list, got {type(cells).__name__}"
    return cells


def select_best_cell(*, cells: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the cell with the highest DSI on the Pareto front."""
    feasible = [
        c
        for c in cells
        if bool(c.get("is_feasible", True)) and not bool(c.get("is_unstable", False))
    ]
    pool = feasible if len(feasible) > 0 else cells
    return max(pool, key=lambda c: float(c.get("dsi", 0.0)))


def cell_record_to_param_vector(*, cell: dict[str, Any]) -> ParameterVector:
    """Convert a Pareto-cell record into a ``ParameterVector`` of the right shape."""
    raw = cell["params"]
    assert isinstance(raw, list), f"expected a list of params, got {type(raw).__name__}"
    vals = np.array([float(x) for x in raw], dtype=np.float64)
    assert vals.shape == (N_PARAMS,), f"params shape {vals.shape} != ({N_PARAMS},)"
    return ParameterVector(values=vals)


def load_t0083_best_cell_param_vector(*, path: Path = T0083_PARETO_FRONT_JSON) -> ParameterVector:
    cells = load_t0083_pareto_cells(path=path)
    best = select_best_cell(cells=cells)
    return cell_record_to_param_vector(cell=best)


if __name__ == "__main__":
    pv = load_t0083_best_cell_param_vector()
    print(f"loaded best-cell ParameterVector with {pv.values.shape[0]} dims")
    print(f"first 5 values: {pv.values[:5].tolist()}")
