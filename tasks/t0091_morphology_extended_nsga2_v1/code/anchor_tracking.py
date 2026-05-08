"""Anchor-tracking analysis (REQ-13, REQ-14).

For each Pareto cell:
* Normalise the 14-d morphology vector (skipping `morph_seed` non-causal dim)
  via min-max against MORPHOLOGY_LOWER_BOUNDS / MORPHOLOGY_UPPER_BOUNDS.
* Compute Euclidean distance to each of the 5 anchors' normalised vectors;
  assign the cell to the nearest.
* Compute v_opt = 2 * lambda_um / tau_m_s (REQ-14, simple cable approximation).
* Tabulate per-anchor counts; bootstrap 1000 resamples for 95% CIs.
* Compute one-sided exact p-value for "anchor 3 (pd_asymmetric) over-represented
  vs anchor 4 (nd_asymmetric)" via permutation test.
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from tasks.t0091_morphology_extended_nsga2_v1.code.anchor_definitions import (
    anchor_to_14d_vector,
    get_anchors,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.constants_t91 import (
    ANCHOR_NAMES,
    MORPHOLOGY_LOWER_BOUNDS,
    MORPHOLOGY_UPPER_BOUNDS,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.paths import (
    ANCHOR_TRACKING_BAR_PNG,
    ANCHOR_TRACKING_JSON,
    PARETO_FRONT_JSON,
    ensure_directories,
)

# Skip morph_seed (index 12) from distance metric — non-causal.
SEED_INDEX_IN_14D: int = 12


def _normalise_14d(*, vector: NDArray[np.float64]) -> NDArray[np.float64]:
    """Min-max normalise 14-d morphology vector, skipping morph_seed."""
    rng_arr = MORPHOLOGY_UPPER_BOUNDS - MORPHOLOGY_LOWER_BOUNDS
    rng_arr = np.where(rng_arr <= 0, 1.0, rng_arr)
    norm = (vector - MORPHOLOGY_LOWER_BOUNDS) / rng_arr
    norm[SEED_INDEX_IN_14D] = 0.0  # mask out seed
    return norm


def _classify_to_anchor(
    *, morph_14d: NDArray[np.float64], anchor_norms: NDArray[np.float64]
) -> int:
    """Return the index of the nearest anchor in normalised 14-d morphology space."""
    norm = _normalise_14d(vector=morph_14d)
    dists = np.linalg.norm(anchor_norms - norm[None, :], axis=1)
    return int(np.argmin(dists))


def _v_opt_um_per_s(*, vector_68d: NDArray[np.float64]) -> float:
    """Simple cable-theoretic v_opt = 2 * lambda / tau_m, where:
    * lambda_um = sqrt(d * R_m / (4 * R_a)) approximated from the 54-d electrophys.
    * tau_m_s = R_m * c_m, with R_m = 1/gleak, c_m = cm_uf_cm2 * 1e-6 F/cm^2.

    For a quick proxy we use:
    * tau_m_ms = c_m / g_leak (in mS/cm^2 conventions)
    * lambda_um proxy = mean_segment_length_um (from 14-d vector index 9 = 54+9=63)
    * v_opt_um_per_s = 2 * lambda_um / tau_m_s
    """
    cm_uf_cm2 = float(vector_68d[35])  # ParamIndex.CM_UF_CM2
    gleak_s_cm2 = float(vector_68d[36])  # ParamIndex.GLEAK_S_CM2
    if gleak_s_cm2 <= 0:
        return float("nan")
    tau_m_s: float = (cm_uf_cm2 * 1e-6) / gleak_s_cm2
    if tau_m_s <= 0:
        return float("nan")
    lambda_um = float(vector_68d[54 + 9])  # mean_segment_length_um
    return 2.0 * lambda_um / tau_m_s


def _effective_dendritic_length_um(*, vector_68d: NDArray[np.float64]) -> float:
    """Proxy for effective dendritic length: branches * mean_segment_length."""
    num_primary = float(vector_68d[54 + 0])
    max_strahler = float(vector_68d[54 + 2])
    mean_seg = float(vector_68d[54 + 9])
    # Crude tree-length approximation: branches per primary = 2^strahler.
    n_branches = num_primary * (2.0 ** max(0.0, max_strahler - 1))
    return float(n_branches * mean_seg)


def _bootstrap_counts(
    *,
    assignments: list[int],
    n_anchors: int,
    n_resamples: int = 1000,
    rng: np.random.Generator,
) -> tuple[list[float], list[float]]:
    """Return (ci95_lo, ci95_hi) per anchor across bootstrap resamples."""
    n_cells = len(assignments)
    if n_cells == 0:
        return [0.0] * n_anchors, [0.0] * n_anchors
    counts_matrix = np.zeros((n_resamples, n_anchors), dtype=np.int64)
    for i in range(n_resamples):
        resampled = rng.choice(assignments, size=n_cells, replace=True)
        for a in range(n_anchors):
            counts_matrix[i, a] = int(np.sum(resampled == a))
    lo = [float(np.percentile(counts_matrix[:, a], 2.5)) for a in range(n_anchors)]
    hi = [float(np.percentile(counts_matrix[:, a], 97.5)) for a in range(n_anchors)]
    return lo, hi


def _exact_pd_vs_nd_pvalue(
    *, assignments: list[int], pd_idx: int = 2, nd_idx: int = 3, rng: np.random.Generator
) -> float:
    """One-sided exact permutation p-value for 'pd_count > nd_count'.

    Null hypothesis: PD/ND assignments are exchangeable. We resample 10000 random
    label permutations of the multiset {pd_count, nd_count} and count how often
    a difference >= observed occurs.
    """
    a = np.asarray(assignments, dtype=np.int32)
    pd_n: int = int(np.sum(a == pd_idx))
    nd_n: int = int(np.sum(a == nd_idx))
    total = pd_n + nd_n
    if total == 0:
        return 1.0
    observed_diff: int = pd_n - nd_n
    n_perm: int = 10000
    extreme_count: int = 0
    for _ in range(n_perm):
        # Each of `total` samples lands in pd vs nd with probability 1/2.
        sim_pd: int = int(rng.binomial(total, 0.5))
        sim_diff: int = sim_pd - (total - sim_pd)
        if sim_diff >= observed_diff:
            extreme_count += 1
    # Add 1 for the observed for unbiasedness.
    return float((extreme_count + 1) / (n_perm + 1))


def main() -> None:
    ensure_directories()
    pareto_payload = json.loads(PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells = pareto_payload["cells"]

    anchors = get_anchors()
    anchor_vectors_14d: list[NDArray[np.float64]] = [
        anchor_to_14d_vector(anchor=anchors[name]) for name in ANCHOR_NAMES
    ]
    anchor_norms = np.vstack([_normalise_14d(vector=v) for v in anchor_vectors_14d])

    rng = np.random.default_rng(seed=42)
    assignments: list[int] = []
    enriched_cells: list[dict[str, object]] = []
    for cell in cells:
        vec_68d = np.array(cell.get("vector_68d") or cell.get("params"), dtype=np.float64)
        morph_14d = (
            vec_68d[54:]
            if len(vec_68d) >= 68
            else np.array(cell.get("morphology_vector_14d", []), dtype=np.float64)
        )
        if morph_14d.shape != (14,):
            morph_14d = np.zeros(14, dtype=np.float64)
        nearest = _classify_to_anchor(morph_14d=morph_14d, anchor_norms=anchor_norms)
        v_opt = _v_opt_um_per_s(vector_68d=vec_68d)
        eff_len = _effective_dendritic_length_um(vector_68d=vec_68d)
        enriched_cells.append(
            {
                **cell,
                "nearest_anchor_index": int(nearest),
                "nearest_anchor_name": ANCHOR_NAMES[nearest],
                "v_opt_um_per_s": float(v_opt),
                "effective_dendritic_length_um": float(eff_len),
            }
        )
        assignments.append(int(nearest))

    n_anchors = len(ANCHOR_NAMES)
    counts_per_anchor: list[int] = [
        int(np.sum(np.array(assignments) == a)) for a in range(n_anchors)
    ]
    ci_lo, ci_hi = _bootstrap_counts(
        assignments=assignments,
        n_anchors=n_anchors,
        n_resamples=1000,
        rng=rng,
    )
    pd_vs_nd_p = _exact_pd_vs_nd_pvalue(
        assignments=assignments,
        pd_idx=2,
        nd_idx=3,
        rng=rng,
    )

    out: dict[str, object] = {
        "n_pareto_cells": len(cells),
        "anchor_names": list(ANCHOR_NAMES),
        "counts_per_anchor": counts_per_anchor,
        "count_ci95_lo": ci_lo,
        "count_ci95_hi": ci_hi,
        "bootstrap_n_resamples": 1000,
        "pd_vs_nd_p_value": pd_vs_nd_p,
        "pd_anchor_index": 2,
        "nd_anchor_index": 3,
        "cells": enriched_cells,
    }
    ANCHOR_TRACKING_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")

    # Bar chart with CIs.
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(n_anchors)
    yerr = np.array(
        [
            [counts_per_anchor[a] - ci_lo[a] for a in range(n_anchors)],
            [ci_hi[a] - counts_per_anchor[a] for a in range(n_anchors)],
        ]
    )
    yerr = np.maximum(yerr, 0.0)
    ax.bar(x, counts_per_anchor, yerr=yerr, capsize=4, color="steelblue")
    ax.set_xticks(x)
    ax.set_xticklabels(ANCHOR_NAMES, rotation=15)
    ax.set_ylabel("Pareto cells assigned (count)")
    ax.set_title(f"Anchor tracking (n={len(cells)}); PD vs ND p={pd_vs_nd_p:.4f} (1000 boot)")
    fig.tight_layout()
    fig.savefig(ANCHOR_TRACKING_BAR_PNG, dpi=150)
    plt.close(fig)

    print(f"[anchor_tracking] counts={counts_per_anchor}; pd_vs_nd_p={pd_vs_nd_p:.4f}")
    print(f"[anchor_tracking] wrote {ANCHOR_TRACKING_JSON}")


if __name__ == "__main__":
    main()
