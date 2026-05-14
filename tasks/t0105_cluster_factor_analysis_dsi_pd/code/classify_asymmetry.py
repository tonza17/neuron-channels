"""Compute normalised asymmetry score per cell and classify symmetric vs asymmetric.

Implements REQ-4. Writes:

* results/data/asym_score_distribution.json
* results/images/asym_score_histogram.png
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (
    ASYM_CLASS_THRESHOLD,
    ASYM_DENOM_BRANCH_DENSITY_GRADIENT,
    ASYM_DENOM_FIELD_ELONGATION,
    ASYM_DENOM_PRIMARY_BRANCH_PD_CONCENTRATION,
    ASYM_DENOM_SOMA_OFFSET,
    ASYM_FIELD_ELONGATION_BASELINE,
    ASYM_THRESHOLD_SWEEP,
    CHART_DPI,
    CLASS_ASYMMETRIC,
    CLASS_SYMMETRIC,
    IDX_BRANCH_DENSITY_GRADIENT_PD,
    IDX_FIELD_ELONGATION_PD,
    IDX_PRIMARY_BRANCH_PD_CONCENTRATION,
    IDX_SOMA_OFFSET_PD_UM,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    ASYM_HISTOGRAM_PATH,
    ASYM_SCORE_DISTRIBUTION_PATH,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
    SELECTED_CELLS_STRICT_PATH,
)


def compute_asym_score(*, vector_68d: list[float]) -> float:
    """Compute the normalised asymmetry score from the 68-d vector."""
    soma_offset: float = vector_68d[IDX_SOMA_OFFSET_PD_UM]
    field_elongation: float = vector_68d[IDX_FIELD_ELONGATION_PD]
    branch_density_gradient: float = vector_68d[IDX_BRANCH_DENSITY_GRADIENT_PD]
    primary_branch_concentration: float = vector_68d[IDX_PRIMARY_BRANCH_PD_CONCENTRATION]
    return (
        abs(soma_offset) / ASYM_DENOM_SOMA_OFFSET
        + abs(field_elongation - ASYM_FIELD_ELONGATION_BASELINE) / ASYM_DENOM_FIELD_ELONGATION
        + abs(branch_density_gradient) / ASYM_DENOM_BRANCH_DENSITY_GRADIENT
        + abs(primary_branch_concentration) / ASYM_DENOM_PRIMARY_BRANCH_PD_CONCENTRATION
    )


def classify_cell(*, asym_score: float, threshold: float = ASYM_CLASS_THRESHOLD) -> str:
    return CLASS_ASYMMETRIC if asym_score >= threshold else CLASS_SYMMETRIC


def _load_cells(*, path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    cells_obj: Any = data["cells"]
    assert isinstance(cells_obj, list)
    out: list[dict[str, Any]] = []
    for c in cells_obj:
        assert isinstance(c, dict)
        out.append(c)
    return out


def _annotate_with_asym(*, cells: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add asym_score and asym_class fields to each cell (mutating)."""
    for cell in cells:
        vec_obj: Any = cell["vector_68d"]
        assert isinstance(vec_obj, list)
        vec: list[float] = [float(v) for v in vec_obj]
        score: float = compute_asym_score(vector_68d=vec)
        cell["asym_score"] = score
        cell["asym_class"] = classify_cell(asym_score=score)
    return cells


def _threshold_sweep(*, scores: list[float]) -> dict[str, dict[str, int]]:
    sweep: dict[str, dict[str, int]] = {}
    for thr in ASYM_THRESHOLD_SWEEP:
        sym = sum(1 for s in scores if s < thr)
        asym = sum(1 for s in scores if s >= thr)
        sweep[f"{thr}"] = {CLASS_SYMMETRIC: sym, CLASS_ASYMMETRIC: asym}
    return sweep


def _plot_histogram(*, scores: list[float], output_path: Path) -> None:
    arr: NDArray[np.float64] = np.array(scores, dtype=np.float64)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    counts, bin_edges, _ = ax.hist(arr, bins=24, color="#4682B4", edgecolor="black", alpha=0.85)
    del counts, bin_edges
    ax.axvline(
        x=ASYM_CLASS_THRESHOLD,
        color="#d62728",
        lw=1.5,
        linestyle="--",
        label=f"class threshold = {ASYM_CLASS_THRESHOLD}",
    )
    ax.set_xlabel("Asymmetry score (range 0 - 4)")
    ax.set_ylabel("Cell count")
    ax.set_title("Distribution of asymmetry scores in the primary cohort")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def _persist_with_asym(*, path: Path, cells: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"cells": cells}, f, indent=2)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    primary_cells: list[dict[str, Any]] = _load_cells(path=SELECTED_CELLS_PRIMARY_PATH)
    strict_cells: list[dict[str, Any]] = _load_cells(path=SELECTED_CELLS_STRICT_PATH)

    primary_annotated: list[dict[str, Any]] = _annotate_with_asym(cells=primary_cells)
    strict_annotated: list[dict[str, Any]] = _annotate_with_asym(cells=strict_cells)

    _persist_with_asym(path=SELECTED_CELLS_PRIMARY_PATH, cells=primary_annotated)
    _persist_with_asym(path=SELECTED_CELLS_STRICT_PATH, cells=strict_annotated)

    primary_scores: list[float] = [float(c["asym_score"]) for c in primary_annotated]
    primary_classes: list[str] = [str(c["asym_class"]) for c in primary_annotated]

    symmetric_count: int = sum(1 for c in primary_classes if c == CLASS_SYMMETRIC)
    asymmetric_count: int = sum(1 for c in primary_classes if c == CLASS_ASYMMETRIC)

    score_arr: NDArray[np.float64] = np.array(primary_scores, dtype=np.float64)
    hist_counts, hist_edges = np.histogram(score_arr, bins=24)

    sweep: dict[str, dict[str, int]] = _threshold_sweep(scores=primary_scores)

    out: dict[str, Any] = {
        "n_primary_cohort": len(primary_annotated),
        "headline_threshold": ASYM_CLASS_THRESHOLD,
        "symmetric_count": symmetric_count,
        "asymmetric_count": asymmetric_count,
        "asym_score_min": float(score_arr.min()),
        "asym_score_max": float(score_arr.max()),
        "asym_score_mean": float(score_arr.mean()),
        "asym_score_median": float(np.median(score_arr)),
        "histogram_bin_edges": hist_edges.tolist(),
        "histogram_counts": hist_counts.tolist(),
        "threshold_sweep": sweep,
    }
    with open(ASYM_SCORE_DISTRIBUTION_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    _plot_histogram(scores=primary_scores, output_path=ASYM_HISTOGRAM_PATH)

    print(f"Primary cohort: N={len(primary_annotated)}")
    print(f"  symmetric (asym < {ASYM_CLASS_THRESHOLD}): {symmetric_count}")
    print(f"  asymmetric (asym >= {ASYM_CLASS_THRESHOLD}): {asymmetric_count}")
    print(
        f"  asym_score: min={out['asym_score_min']:.3f} max={out['asym_score_max']:.3f} "
        f"mean={out['asym_score_mean']:.3f} median={out['asym_score_median']:.3f}"
    )
    print()
    print("Threshold sweep (primary cohort):")
    for thr_str, counts in sweep.items():
        print(f"  thr={thr_str}: sym={counts[CLASS_SYMMETRIC]} asym={counts[CLASS_ASYMMETRIC]}")
    print()
    print(f"Wrote: {ASYM_SCORE_DISTRIBUTION_PATH}")
    print(f"Wrote: {ASYM_HISTOGRAM_PATH}")
    print(f"Annotated cells written back: {SELECTED_CELLS_PRIMARY_PATH}")


if __name__ == "__main__":
    main()
