"""Build the 5-anchor x 19-electrophys-clone warm-start population (REQ-3, REQ-4).

Reads t0083 `pareto_front.json` (18 cells); reads t0086 `cell_classification.json`
(Genuine + Marginal labels per cell). For each anchor's 14-d morphology vector,
sample 19 electrophys vectors from the t0083 Pareto preferring Genuine then
Marginal cells; if 18 < 19 needed, fall back to Pareto cells with replacement.
Project each electrophys vector against `LOWER_BOUNDS_54` / `UPPER_BOUNDS_54`
(clamp into bounds). Concatenate the 14-d morphology vector with the 54-d
electrophys vector for each (anchor, clone) pair to produce a 68-d row. Add 1
random LHS sample drawn against the 68-d bounds (last cell). Pack into a
`(96, 68)` numpy array.
"""

from __future__ import annotations

import json

import numpy as np
from numpy.typing import NDArray

from tasks.t0091_morphology_extended_nsga2_v1.code.anchor_definitions import (
    anchor_to_14d_vector,
    get_anchors,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.constants import (
    LOWER_BOUNDS as LOWER_BOUNDS_54,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.constants import (
    UPPER_BOUNDS as UPPER_BOUNDS_54,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.constants_t91 import (
    ANCHOR_NAMES,
    LOWER_BOUNDS_68,
    N_ANCHORS,
    N_CLONES_PER_ANCHOR,
    N_PARAMS_54,
    N_RANDOM_FILL,
    POP_SIZE,
    UPPER_BOUNDS_68,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.paths import (
    T0083_PARETO_FRONT_JSON,
    T0086_CELL_CLASSIFICATION_JSON,
    WARM_START_POPULATION_JSON,
    ensure_directories,
)


def _load_t0083_pareto_cells() -> list[dict[str, object]]:
    """Return the t0083 Pareto cell list with `params` (54-d) preserved."""
    payload = json.loads(T0083_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells: list[dict[str, object]] = list(payload["cells"])
    return cells


def _load_t0086_classification() -> dict[int, str]:
    """Map t0083 `cell_index` -> classification label ('Genuine'/'Marginal'/...)."""
    if not T0086_CELL_CLASSIFICATION_JSON.exists():
        return {}
    payload = json.loads(T0086_CELL_CLASSIFICATION_JSON.read_text(encoding="utf-8"))
    out: dict[int, str] = {}
    items = payload.get("classifications") or payload.get("cells") or []
    for item in items:
        cid = item.get("cell_index")
        label = item.get("classification") or item.get("class") or item.get("label")
        if cid is not None and label is not None:
            out[int(cid)] = str(label)
    return out


def _classification_priority(*, label: str | None) -> int:
    """Lower is better: Genuine < Marginal < Stochastic / unknown."""
    if label is None:
        return 99
    label_lower = label.lower()
    if "genuine" in label_lower:
        return 0
    if "marginal" in label_lower:
        return 1
    return 50


def _clip_54d(vec: NDArray[np.float64]) -> NDArray[np.float64]:
    """Clamp a 54-d vector into the t0080 bounds."""
    return np.clip(vec, LOWER_BOUNDS_54, UPPER_BOUNDS_54)


def _select_electrophys_clones(
    *, n_clones: int, rng: np.random.Generator
) -> list[tuple[int, NDArray[np.float64]]]:
    """Select n_clones electrophys vectors from t0083 Pareto, preferring Genuine."""
    cells = _load_t0083_pareto_cells()
    classifications = _load_t0086_classification()

    # Sort by classification priority (Genuine first), with stable tiebreaker on
    # cell_index for determinism.
    cells_with_priority = sorted(
        cells,
        key=lambda c: (
            _classification_priority(label=classifications.get(int(c["cell_index"]))),
            int(c["cell_index"]),
        ),
    )

    chosen: list[tuple[int, NDArray[np.float64]]] = []
    n_unique = min(n_clones, len(cells_with_priority))
    for i in range(n_unique):
        cell = cells_with_priority[i]
        chosen.append(
            (
                int(cell["cell_index"]),
                _clip_54d(np.asarray(cell["params"], dtype=np.float64)),
            )
        )
    # If we need more than the unique count, sample with replacement.
    if n_clones > n_unique:
        for _ in range(n_clones - n_unique):
            idx = int(rng.integers(0, len(cells_with_priority)))
            cell = cells_with_priority[idx]
            chosen.append(
                (
                    int(cell["cell_index"]),
                    _clip_54d(np.asarray(cell["params"], dtype=np.float64)),
                )
            )
    assert len(chosen) == n_clones
    return chosen


def build_warmstart_population() -> tuple[NDArray[np.float64], list[dict[str, object]]]:
    """Build the (96, 68) warm-start population matrix.

    Returns (matrix, metadata) where metadata lists per-row anchor/source info.
    """
    rng = np.random.default_rng(seed=42)
    anchors = get_anchors()
    anchor_vectors_14d: list[NDArray[np.float64]] = [
        anchor_to_14d_vector(anchor=anchors[name]) for name in ANCHOR_NAMES
    ]

    matrix = np.zeros((POP_SIZE, 68), dtype=np.float64)
    metadata: list[dict[str, object]] = []

    row = 0
    for anchor_idx, name in enumerate(ANCHOR_NAMES):
        morph_14d = anchor_vectors_14d[anchor_idx]
        clones = _select_electrophys_clones(n_clones=N_CLONES_PER_ANCHOR, rng=rng)
        for clone_idx, (src_cell_index, electrophys_54d) in enumerate(clones):
            assert electrophys_54d.shape == (N_PARAMS_54,)
            matrix[row, :N_PARAMS_54] = electrophys_54d
            matrix[row, N_PARAMS_54:] = morph_14d
            metadata.append(
                {
                    "row": row,
                    "anchor_index": anchor_idx,
                    "anchor_name": name,
                    "clone_index": clone_idx,
                    "source_t0083_cell_index": src_cell_index,
                }
            )
            row += 1

    # Random fill for the last N_RANDOM_FILL slots — uniform LHS-style draw.
    for fill_idx in range(N_RANDOM_FILL):
        rand = rng.uniform(LOWER_BOUNDS_68, UPPER_BOUNDS_68)
        matrix[row] = rand
        metadata.append(
            {
                "row": row,
                "anchor_index": -1,
                "anchor_name": "random",
                "clone_index": fill_idx,
                "source_t0083_cell_index": None,
            }
        )
        row += 1

    assert row == POP_SIZE, f"warmstart row count {row} != expected {POP_SIZE}"
    # Final clamp to be safe.
    matrix = np.clip(matrix, LOWER_BOUNDS_68, UPPER_BOUNDS_68)
    return matrix, metadata


def main() -> None:
    ensure_directories()
    matrix, metadata = build_warmstart_population()
    out: dict[str, object] = {
        "shape": list(matrix.shape),
        "n_anchors": N_ANCHORS,
        "n_clones_per_anchor": N_CLONES_PER_ANCHOR,
        "n_random_fill": N_RANDOM_FILL,
        "metadata": metadata,
        "matrix": matrix.tolist(),
    }
    WARM_START_POPULATION_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[warmstart] wrote {WARM_START_POPULATION_JSON} shape={matrix.shape} "
        f"({N_ANCHORS} anchors x {N_CLONES_PER_ANCHOR} clones + {N_RANDOM_FILL} random)"
    )


if __name__ == "__main__":
    main()
