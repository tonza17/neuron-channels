"""Phase C step 2: post-hoc nearest-anchor classification of Pareto cells.

Reads t0091's anchor_definitions.json (5 fixed reference anchors in 14-d
morphology space) and assigns each per-seed Pareto cell to its nearest anchor
using the same min-max-normalised Euclidean distance metric as t0091's
`anchor_tracking.py`. The seed-index dimension (idx 12 in the 14-d morphology
vector) is masked out before computing distance because morph_seed is
non-causal.

Output per seed: ``anchor_tracking_seed{s}.json`` with per-cell records and
per-anchor counts.
"""

from __future__ import annotations

import json

import numpy as np
from numpy.typing import NDArray

from tasks.t0107_t0106_polar_8dir_recheck.code.constants import (
    ANCHOR_NAMES,
    MORPHOLOGY_LOWER_BOUNDS,
    MORPHOLOGY_UPPER_BOUNDS,
    N_ANCHORS,
)
from tasks.t0107_t0106_polar_8dir_recheck.code.paths import (
    T0091_ANCHOR_DEFINITIONS_JSON,
    anchor_tracking_json,
    ensure_directories,
    pareto_front_json,
)

SEED_INDEX_IN_14D: int = 12


def _load_anchor_vectors_14d() -> NDArray[np.float64]:
    """Load the 5 anchor 14-d morphology vectors from t0091's JSON."""
    payload = json.loads(T0091_ANCHOR_DEFINITIONS_JSON.read_text(encoding="utf-8"))
    anchors = payload["anchors"]
    assert len(anchors) == N_ANCHORS, f"expected {N_ANCHORS} anchors, got {len(anchors)}"
    vectors = np.zeros((N_ANCHORS, 14), dtype=np.float64)
    for entry in anchors:
        idx = int(entry["anchor_index"])
        vectors[idx, :] = np.asarray(entry["vector_14d"], dtype=np.float64)
    return vectors


def _normalise_14d(*, vector: NDArray[np.float64]) -> NDArray[np.float64]:
    rng_arr = MORPHOLOGY_UPPER_BOUNDS - MORPHOLOGY_LOWER_BOUNDS
    rng_arr = np.where(rng_arr <= 0, 1.0, rng_arr)
    norm = (vector - MORPHOLOGY_LOWER_BOUNDS) / rng_arr
    norm[SEED_INDEX_IN_14D] = 0.0
    return norm


def _classify(
    *,
    morph_14d: NDArray[np.float64],
    anchor_norms: NDArray[np.float64],
) -> tuple[int, float, list[float]]:
    norm = _normalise_14d(vector=morph_14d)
    dists = np.linalg.norm(anchor_norms - norm[None, :], axis=1)
    nearest = int(np.argmin(dists))
    return nearest, float(dists[nearest]), [float(d) for d in dists.tolist()]


def classify_pareto_for_seed(*, seed: int) -> dict[str, object]:
    pareto = json.loads(pareto_front_json(seed=seed).read_text(encoding="utf-8"))
    cells_in = pareto["cells"]
    anchor_vecs = _load_anchor_vectors_14d()
    anchor_norms = np.array(
        [_normalise_14d(vector=anchor_vecs[i]) for i in range(N_ANCHORS)],
        dtype=np.float64,
    )

    cells_out: list[dict[str, object]] = []
    counts = [0] * N_ANCHORS
    for cell_in in cells_in:
        cell_id = int(cell_in.get("cell_id", -1))
        morph_14d_list = cell_in.get("morphology_vector_14d") or list(
            cell_in.get("vector_68d", [])[54:]
        )
        morph_14d = np.asarray(morph_14d_list, dtype=np.float64)
        nearest_idx, nearest_dist, all_dists = _classify(
            morph_14d=morph_14d, anchor_norms=anchor_norms
        )
        counts[nearest_idx] += 1
        cells_out.append(
            {
                "cell_id": cell_id,
                "morphology_vector_14d": [float(v) for v in morph_14d],
                "nearest_anchor_index": nearest_idx,
                "nearest_anchor_name": ANCHOR_NAMES[nearest_idx],
                "nearest_anchor_distance_normalised": nearest_dist,
                "all_anchor_distances_normalised": all_dists,
            }
        )

    return {
        "seed": seed,
        "anchor_names": list(ANCHOR_NAMES),
        "n_cells": len(cells_out),
        "counts_per_anchor": counts,
        "cells": cells_out,
    }


def main_for_seed(*, seed: int) -> dict[str, object]:
    ensure_directories()
    payload = classify_pareto_for_seed(seed=seed)
    out_path = anchor_tracking_json(seed=seed)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        f"[anchor_classifier seed={seed}] wrote {out_path}: "
        f"{payload['n_cells']} cells; counts {payload['counts_per_anchor']}"
    )
    return payload


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Classify Pareto cells to t0091 anchors")
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    main_for_seed(seed=int(args.seed))
