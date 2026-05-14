"""Pearson r between factor scores and DSI / PD, identify joint factor.

Implements REQ-9. Outputs (primary cohort):

* results/data/factor_correlations.json
* results/images/factor_correlations.png
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.stats import pearsonr

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import CHART_DPI
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    FACTOR_CORRELATIONS_CHART_PATH,
    FACTOR_CORRELATIONS_PATH,
    FACTOR_SCORES_PATH,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
)

JOINT_R_THRESHOLD: float = 0.3


@dataclass(frozen=True, slots=True)
class FactorCorrelation:
    factor_index: int
    r_dsi: float
    p_dsi: float
    r_pd: float
    p_pd: float


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


def _load_scores(*, path: Path) -> NDArray[np.float64]:
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    scores_obj: Any = data["scores"]
    return np.asarray(scores_obj, dtype=np.float64)


def compute_correlations(
    *,
    scores: NDArray[np.float64],
    dsi: NDArray[np.float64],
    pd_rate: NDArray[np.float64],
) -> list[FactorCorrelation]:
    n_factors: int = scores.shape[1]
    out: list[FactorCorrelation] = []
    for fac_idx in range(n_factors):
        col: NDArray[np.float64] = scores[:, fac_idx]
        r_dsi, p_dsi = pearsonr(col, dsi)
        r_pd, p_pd = pearsonr(col, pd_rate)
        out.append(
            FactorCorrelation(
                factor_index=fac_idx,
                r_dsi=float(r_dsi),
                p_dsi=float(p_dsi),
                r_pd=float(r_pd),
                p_pd=float(p_pd),
            )
        )
    return out


def top3_by_abs(*, correlations: list[FactorCorrelation], outcome: str) -> list[dict[str, Any]]:
    if outcome == "dsi":
        keyed = sorted(correlations, key=lambda c: -abs(c.r_dsi))[:3]
        return [{"factor": f"F{c.factor_index + 1}", "r": c.r_dsi, "p": c.p_dsi} for c in keyed]
    if outcome == "pd":
        keyed = sorted(correlations, key=lambda c: -abs(c.r_pd))[:3]
        return [{"factor": f"F{c.factor_index + 1}", "r": c.r_pd, "p": c.p_pd} for c in keyed]
    raise ValueError(f"unknown outcome: {outcome}")


def find_joint_factors(
    *,
    correlations: list[FactorCorrelation],
    threshold: float = JOINT_R_THRESHOLD,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for c in correlations:
        if abs(c.r_dsi) > threshold and abs(c.r_pd) > threshold:
            out.append(
                {
                    "factor": f"F{c.factor_index + 1}",
                    "r_dsi": c.r_dsi,
                    "p_dsi": c.p_dsi,
                    "r_pd": c.r_pd,
                    "p_pd": c.p_pd,
                }
            )
    return out


def _plot_correlations(
    *,
    correlations: list[FactorCorrelation],
    output_path: Path,
    title_suffix: str,
) -> None:
    n_factors: int = len(correlations)
    xs: NDArray[np.float64] = np.arange(n_factors, dtype=np.float64)
    bar_w: float = 0.4
    fig, ax = plt.subplots(figsize=(max(6.0, n_factors * 0.8), 4.5))
    r_dsi: list[float] = [abs(c.r_dsi) for c in correlations]
    r_pd: list[float] = [abs(c.r_pd) for c in correlations]
    ax.bar(xs - bar_w / 2, r_dsi, bar_w, color="#1f77b4", label="|r| vs DSI")
    ax.bar(xs + bar_w / 2, r_pd, bar_w, color="#d62728", label="|r| vs PD")
    ax.axhline(
        y=JOINT_R_THRESHOLD,
        color="#888888",
        lw=1.0,
        linestyle="--",
        label=f"joint-factor threshold |r| = {JOINT_R_THRESHOLD}",
    )
    ax.set_xticks(xs)
    ax.set_xticklabels([f"F{c.factor_index + 1}" for c in correlations])
    ax.set_ylabel("|Pearson r|")
    ax.set_xlabel("Factor")
    ax.set_title(f"Factor correlation with DSI and PD {title_suffix}")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)


def write_outputs(
    *,
    correlations: list[FactorCorrelation],
    out_path: Path,
) -> None:
    payload: dict[str, Any] = {
        "n_factors": len(correlations),
        "joint_r_threshold": JOINT_R_THRESHOLD,
        "per_factor": [
            {
                "factor": f"F{c.factor_index + 1}",
                "factor_index": c.factor_index,
                "r_dsi": c.r_dsi,
                "p_dsi": c.p_dsi,
                "r_pd": c.r_pd,
                "p_pd": c.p_pd,
            }
            for c in correlations
        ],
        "top3_dsi": top3_by_abs(correlations=correlations, outcome="dsi"),
        "top3_pd": top3_by_abs(correlations=correlations, outcome="pd"),
        "joint_factors": find_joint_factors(correlations=correlations),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    cells: list[dict[str, Any]] = _load_cells(path=SELECTED_CELLS_PRIMARY_PATH)
    scores: NDArray[np.float64] = _load_scores(path=FACTOR_SCORES_PATH)
    dsi: NDArray[np.float64] = np.array([float(c["dsi"]) for c in cells], dtype=np.float64)
    pd_rate: NDArray[np.float64] = np.array(
        [float(c["pd_rate_hz"]) for c in cells], dtype=np.float64
    )
    assert scores.shape[0] == len(cells), f"scores rows {scores.shape[0]} != n_cells {len(cells)}"

    correlations: list[FactorCorrelation] = compute_correlations(
        scores=scores, dsi=dsi, pd_rate=pd_rate
    )
    print(f"Computed Pearson r for {len(correlations)} factors against DSI and PD.")
    for c in correlations:
        print(
            f"  F{c.factor_index + 1}: "
            f"r_DSI={c.r_dsi:+.3f} (p={c.p_dsi:.3g})  "
            f"r_PD={c.r_pd:+.3f} (p={c.p_pd:.3g})"
        )
    top3_d = top3_by_abs(correlations=correlations, outcome="dsi")
    top3_p = top3_by_abs(correlations=correlations, outcome="pd")
    joint = find_joint_factors(correlations=correlations)
    print()
    print("Top-3 factors by |r| vs DSI:")
    for entry in top3_d:
        print(f"  {entry['factor']}: r={entry['r']:+.3f} p={entry['p']:.3g}")
    print("Top-3 factors by |r| vs PD:")
    for entry in top3_p:
        print(f"  {entry['factor']}: r={entry['r']:+.3f} p={entry['p']:.3g}")
    print(f"Joint factors (|r_DSI| > 0.3 AND |r_PD| > 0.3): {len(joint)}")
    for j in joint:
        print(f"  {j['factor']}: r_DSI={j['r_dsi']:+.3f}, r_PD={j['r_pd']:+.3f}")

    write_outputs(correlations=correlations, out_path=FACTOR_CORRELATIONS_PATH)
    _plot_correlations(
        correlations=correlations,
        output_path=FACTOR_CORRELATIONS_CHART_PATH,
        title_suffix="(primary cohort)",
    )
    print()
    print(f"Wrote: {FACTOR_CORRELATIONS_PATH}")
    print(f"Wrote: {FACTOR_CORRELATIONS_CHART_PATH}")


if __name__ == "__main__":
    main()
