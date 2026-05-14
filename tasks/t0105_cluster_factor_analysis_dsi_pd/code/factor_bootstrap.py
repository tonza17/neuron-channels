"""Bootstrap factor loadings (200 resamples) with alignment to the headline fit.

Implements REQ-10. Outputs:

* results/data/factor_bootstrap.json
* results/images/factor_loadings_bootstrap.png
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (
    ALL_PARAM_NAMES,
    BOOTSTRAP_RESAMPLES,
    CHART_DPI,
    KAISER_FACTOR_CAP,
    N_TOTAL_DIMS,
    RANDOM_SEED,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.factor_analysis import (
    run_factor_pipeline,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    FACTOR_BOOTSTRAP_PATH,
    FACTOR_BOOTSTRAP_PATH_PNG,
    FACTOR_LOADINGS_PATH,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
)

STABILITY_SIGN_FRACTION: float = 0.90
STABILITY_LOADING_MAGNITUDE: float = 0.4
TOP_K_PER_FACTOR: int = 5


@dataclass(frozen=True, slots=True)
class AlignmentResult:
    permutation: list[int]
    sign_flips: list[int]


def _align_loadings(
    *,
    headline: NDArray[np.float64],
    candidate: NDArray[np.float64],
) -> tuple[NDArray[np.float64], AlignmentResult]:
    """Align candidate factor columns to headline by maximising row-wise dot products.

    Returns the aligned candidate loadings (same shape) and the permutation + sign
    flips applied. Greedy assignment: for each headline column, pick the unused
    candidate column maximising |dot product| (NaN-safe).
    """
    n_factors: int = headline.shape[1]
    assert candidate.shape == headline.shape, (
        f"shape mismatch: {candidate.shape} vs {headline.shape}"
    )
    head_safe: NDArray[np.float64] = np.where(np.isnan(headline), 0.0, headline)
    cand_safe: NDArray[np.float64] = np.where(np.isnan(candidate), 0.0, candidate)
    dots: NDArray[np.float64] = head_safe.T @ cand_safe  # (k, k)
    used: set[int] = set()
    permutation: list[int] = [-1] * n_factors
    sign_flips: list[int] = [1] * n_factors
    for i in range(n_factors):
        # Best unused candidate column by |dot|.
        scores: NDArray[np.float64] = np.where(
            np.array([j in used for j in range(n_factors)]),
            -np.inf,
            np.abs(dots[i, :]),
        )
        best_j: int = int(np.argmax(scores))
        used.add(best_j)
        permutation[i] = best_j
        sign_flips[i] = 1 if dots[i, best_j] >= 0.0 else -1
    aligned: NDArray[np.float64] = np.zeros_like(candidate)
    for i in range(n_factors):
        aligned[:, i] = candidate[:, permutation[i]] * float(sign_flips[i])
    return aligned, AlignmentResult(permutation=permutation, sign_flips=sign_flips)


def _load_headline_loadings(*, path: Path) -> NDArray[np.float64]:
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    loadings_obj: Any = data["loadings"]
    n_factors: int = int(data["n_factors"])
    out: NDArray[np.float64] = np.full(
        (N_TOTAL_DIMS, n_factors), fill_value=np.nan, dtype=np.float64
    )
    for i, row in enumerate(loadings_obj):
        for j, v in enumerate(row):
            out[i, j] = float(v) if v is not None else np.nan
    return out


def _load_cells(*, path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    cells_obj: Any = data["cells"]
    assert isinstance(cells_obj, list)
    return [c for c in cells_obj if isinstance(c, dict)]


def run_bootstrap(
    *,
    cells: list[dict[str, Any]],
    headline_loadings: NDArray[np.float64],
    n_resamples: int = BOOTSTRAP_RESAMPLES,
    random_seed: int = RANDOM_SEED,
) -> tuple[NDArray[np.float64], int]:
    """Run bootstrap. Returns (aligned_loadings_stack (R, P, K), n_failed)."""
    rng: np.random.Generator = np.random.default_rng(random_seed)
    n_cells: int = len(cells)
    n_factors: int = headline_loadings.shape[1]
    stack: NDArray[np.float64] = np.full(
        (n_resamples, N_TOTAL_DIMS, n_factors), fill_value=np.nan, dtype=np.float64
    )
    n_failed: int = 0
    for r_idx in tqdm(range(n_resamples), desc="bootstrap"):
        idx: NDArray[np.intp] = rng.integers(0, n_cells, size=n_cells)
        resample_cells: list[dict[str, Any]] = [cells[int(i)] for i in idx]
        try:
            fa_out, _, _ = run_factor_pipeline(cells=resample_cells, factor_cap=KAISER_FACTOR_CAP)
        except (ValueError, np.linalg.LinAlgError):
            n_failed += 1
            continue
        # Pad / truncate loadings to match headline n_factors (different cohorts
        # may pick different Kaiser counts; rare for resamples).
        cand: NDArray[np.float64] = fa_out.loadings
        if cand.shape[1] != n_factors:
            if cand.shape[1] > n_factors:
                cand = cand[:, :n_factors]
            else:
                pad_n: int = n_factors - cand.shape[1]
                pad: NDArray[np.float64] = np.full((N_TOTAL_DIMS, pad_n), np.nan)
                cand = np.concatenate([cand, pad], axis=1)
        aligned, _ = _align_loadings(headline=headline_loadings, candidate=cand)
        stack[r_idx, :, :] = aligned
    return stack, n_failed


def compute_cis_and_stability(
    *,
    stack: NDArray[np.float64],
    headline_loadings: NDArray[np.float64],
    sign_fraction: float = STABILITY_SIGN_FRACTION,
    magnitude_threshold: float = STABILITY_LOADING_MAGNITUDE,
    top_k: int = TOP_K_PER_FACTOR,
) -> dict[str, Any]:
    n_factors: int = headline_loadings.shape[1]
    # Percentile CIs (treating NaNs from failed resamples as missing).
    lo_pct: NDArray[np.float64] = np.nanpercentile(stack, 2.5, axis=0)
    hi_pct: NDArray[np.float64] = np.nanpercentile(stack, 97.5, axis=0)
    median: NDArray[np.float64] = np.nanmedian(stack, axis=0)

    # Determine stable factors.
    stable_factors: list[dict[str, Any]] = []
    per_factor_details: list[dict[str, Any]] = []
    for fac_idx in range(n_factors):
        head_col: NDArray[np.float64] = headline_loadings[:, fac_idx]
        # Top-K by headline absolute loading (NaN-safe).
        head_abs: NDArray[np.float64] = np.where(np.isnan(head_col), 0.0, np.abs(head_col))
        order: NDArray[np.intp] = np.argsort(-head_abs)[:top_k]
        per_dim_details: list[dict[str, Any]] = []
        all_consistent: bool = True
        magnitudes_ok: bool = True
        for j in order:
            jj: int = int(j)
            head_v: float = float(head_col[jj]) if not np.isnan(head_col[jj]) else 0.0
            samples: NDArray[np.float64] = stack[:, jj, fac_idx]
            samples_clean: NDArray[np.float64] = samples[~np.isnan(samples)]
            sign_consistency: float = (
                0.0
                if samples_clean.size == 0
                else float(np.mean(np.sign(samples_clean) == np.sign(head_v)))
            )
            median_abs_loading: float = (
                float(np.median(np.abs(samples_clean))) if samples_clean.size > 0 else 0.0
            )
            if sign_consistency < sign_fraction:
                all_consistent = False
            if median_abs_loading < magnitude_threshold:
                magnitudes_ok = False
            per_dim_details.append(
                {
                    "param_index": jj,
                    "param_name": ALL_PARAM_NAMES[jj],
                    "headline_loading": head_v,
                    "median_loading": float(median[jj, fac_idx]),
                    "ci_low": float(lo_pct[jj, fac_idx]),
                    "ci_high": float(hi_pct[jj, fac_idx]),
                    "sign_consistency": sign_consistency,
                    "median_abs_loading": median_abs_loading,
                }
            )
        is_stable: bool = all_consistent and magnitudes_ok
        per_factor_details.append(
            {
                "factor": f"F{fac_idx + 1}",
                "factor_index": fac_idx,
                "stable": is_stable,
                "top_loadings": per_dim_details,
            }
        )
        if is_stable:
            stable_factors.append({"factor": f"F{fac_idx + 1}", "factor_index": fac_idx})

    return {
        "median_loadings": median.tolist(),
        "ci_low": lo_pct.tolist(),
        "ci_high": hi_pct.tolist(),
        "per_factor_details": per_factor_details,
        "stable_factors": stable_factors,
        "stability_sign_fraction": sign_fraction,
        "stability_magnitude_threshold": magnitude_threshold,
    }


def _plot_bootstrap(
    *,
    headline_loadings: NDArray[np.float64],
    median_loadings: NDArray[np.float64],
    ci_low: NDArray[np.float64],
    ci_high: NDArray[np.float64],
    per_factor_details: list[dict[str, Any]],
    output_path: Path,
) -> None:
    n_factors: int = headline_loadings.shape[1]
    fig, axes = plt.subplots(n_factors, 1, figsize=(8.0, max(8.0, n_factors * 1.8)), sharex=False)
    axes_list: list[plt.Axes] = list(np.atleast_1d(axes))
    for fac_idx in range(n_factors):
        ax: plt.Axes = axes_list[fac_idx]
        entries: list[dict[str, Any]] = per_factor_details[fac_idx]["top_loadings"]
        names: list[str] = [str(e["param_name"]) for e in entries]
        head_vals: list[float] = [float(e["headline_loading"]) for e in entries]
        med_vals: list[float] = [float(e["median_loading"]) for e in entries]
        low_vals: list[float] = [float(e["ci_low"]) for e in entries]
        high_vals: list[float] = [float(e["ci_high"]) for e in entries]
        xs: NDArray[np.float64] = np.arange(len(entries), dtype=np.float64)
        err_low: NDArray[np.float64] = np.array(
            [float(med_vals[i] - low_vals[i]) for i in range(len(entries))]
        )
        err_high: NDArray[np.float64] = np.array(
            [float(high_vals[i] - med_vals[i]) for i in range(len(entries))]
        )
        err_low = np.maximum(err_low, 0.0)
        err_high = np.maximum(err_high, 0.0)
        err: NDArray[np.float64] = np.vstack([err_low, err_high])
        ax.errorbar(
            xs,
            med_vals,
            yerr=err,
            fmt="o",
            color="#2ca02c",
            ecolor="#888888",
            markersize=8,
            capsize=4,
            label="bootstrap median + 95% CI",
        )
        ax.scatter(
            xs,
            head_vals,
            marker="x",
            color="#d62728",
            s=80,
            label="headline",
        )
        ax.axhline(y=0.0, color="black", lw=0.5)
        stable_label: str = " (stable)" if per_factor_details[fac_idx]["stable"] else ""
        ax.set_title(f"F{fac_idx + 1}{stable_label}: top-5 loadings", fontsize=9)
        ax.set_xticks(xs)
        ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("Loading")
        if fac_idx == 0:
            ax.legend(loc="upper right", fontsize=8)
    fig.suptitle(
        f"Bootstrap factor-loading 95% CIs ({BOOTSTRAP_RESAMPLES} resamples)",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    cells: list[dict[str, Any]] = _load_cells(path=SELECTED_CELLS_PRIMARY_PATH)
    headline: NDArray[np.float64] = _load_headline_loadings(path=FACTOR_LOADINGS_PATH)
    n_factors: int = headline.shape[1]
    print(
        f"Bootstrap: N_cells={len(cells)} n_factors={n_factors} "
        f"n_resamples={BOOTSTRAP_RESAMPLES} seed={RANDOM_SEED}"
    )

    start: float = time.perf_counter()
    stack, n_failed = run_bootstrap(
        cells=cells, headline_loadings=headline, n_resamples=BOOTSTRAP_RESAMPLES
    )
    elapsed: float = time.perf_counter() - start
    print(f"  bootstrap completed in {elapsed:.1f} s ({n_failed} resamples failed)")

    summary: dict[str, Any] = compute_cis_and_stability(
        stack=stack,
        headline_loadings=headline,
    )
    summary_full: dict[str, Any] = {
        "n_bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "n_resamples_failed": n_failed,
        "elapsed_seconds": elapsed,
        "random_seed": RANDOM_SEED,
        **summary,
    }
    with open(FACTOR_BOOTSTRAP_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_full, f, indent=2)

    _plot_bootstrap(
        headline_loadings=headline,
        median_loadings=np.asarray(summary["median_loadings"]),
        ci_low=np.asarray(summary["ci_low"]),
        ci_high=np.asarray(summary["ci_high"]),
        per_factor_details=summary["per_factor_details"],
        output_path=FACTOR_BOOTSTRAP_PATH_PNG,
    )

    print()
    print(f"Stable factors: {[s['factor'] for s in summary['stable_factors']]}")
    print(f"Wrote: {FACTOR_BOOTSTRAP_PATH}")
    print(f"Wrote: {FACTOR_BOOTSTRAP_PATH_PNG}")


if __name__ == "__main__":
    main()
