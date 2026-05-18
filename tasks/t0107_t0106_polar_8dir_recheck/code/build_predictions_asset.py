"""Materialise the t0107 predictions asset from the polar evaluation output.

Reads `results/data/per_cell_polar_eval.json`, computes per-cell DSI summary
statistics for `metrics_at_creation`, and writes:

* `assets/predictions/eight-dir-polar-recheck-top10-t0106/details.json`
* `assets/predictions/eight-dir-polar-recheck-top10-t0106/description.md`
* `assets/predictions/eight-dir-polar-recheck-top10-t0106/files/per_cell_polar_eval.json`

The schema and section layout follow `meta/asset_types/predictions/specification.md` v2.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from scipy import stats  # type: ignore[import-untyped]

from tasks.t0107_t0106_polar_8dir_recheck.code.paths import (
    RESULTS_DATA_DIR,
    TASK_ROOT,
)

PREDICTIONS_ID: str = "eight-dir-polar-recheck-top10-t0106"
ASSET_DIR: Path = TASK_ROOT / "assets" / "predictions" / PREDICTIONS_ID
DETAILS_JSON: Path = ASSET_DIR / "details.json"
DESCRIPTION_MD: Path = ASSET_DIR / "description.md"
FILES_DIR: Path = ASSET_DIR / "files"
PER_CELL_POLAR_DEST: Path = FILES_DIR / "per_cell_polar_eval.json"
PER_CELL_POLAR_SOURCE: Path = RESULTS_DATA_DIR / "per_cell_polar_eval.json"

DATE_CREATED: str = "2026-05-18"


@dataclass(frozen=True, slots=True)
class CellSummary:
    t0106_rank: int
    t0106_dsi: float
    t0107_dsi_8dir_vsum: float
    t0107_pd_at_0deg: float
    t0107_nd_at_180deg: float
    t0107_dsi_2dir_ratio_sanity: float


def _load_summary(*, path: Path) -> list[CellSummary]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records: list[dict[str, object]] = payload["evaluations"]  # type: ignore[index]
    out: list[CellSummary] = []
    for r in records:
        out.append(
            CellSummary(
                t0106_rank=int(r["t0106_rank"]),  # type: ignore[arg-type]
                t0106_dsi=float(r["t0106_dsi"]),  # type: ignore[arg-type]
                t0107_dsi_8dir_vsum=float(r["t0107_dsi_8dir_vsum"]),  # type: ignore[arg-type]
                t0107_pd_at_0deg=float(r["t0107_pd_at_0deg"]),  # type: ignore[arg-type]
                t0107_nd_at_180deg=float(r["t0107_nd_at_180deg"]),  # type: ignore[arg-type]
                t0107_dsi_2dir_ratio_sanity=float(
                    r["t0107_dsi_2dir_ratio_sanity"]  # type: ignore[arg-type]
                ),
            )
        )
    return out


def _compute_summary_metrics(*, cells: list[CellSummary]) -> dict[str, float]:
    dsi_vsum = np.array([c.t0107_dsi_8dir_vsum for c in cells], dtype=np.float64)
    dsi_t0106 = np.array([c.t0106_dsi for c in cells], dtype=np.float64)
    pd0 = np.array([c.t0107_pd_at_0deg for c in cells], dtype=np.float64)
    nd180 = np.array([c.t0107_nd_at_180deg for c in cells], dtype=np.float64)
    ratio = np.array([c.t0107_dsi_2dir_ratio_sanity for c in cells], dtype=np.float64)
    rho_result = stats.spearmanr(dsi_t0106, dsi_vsum)
    rho: float = float(rho_result.statistic)
    pval: float = float(rho_result.pvalue)
    return {
        "n_cells": float(len(cells)),
        "t0107_dsi_8dir_vsum_mean": float(np.mean(dsi_vsum)),
        "t0107_dsi_8dir_vsum_std": float(np.std(dsi_vsum, ddof=1)),
        "t0107_dsi_8dir_vsum_min": float(np.min(dsi_vsum)),
        "t0107_dsi_8dir_vsum_max": float(np.max(dsi_vsum)),
        "t0107_pd_at_0deg_mean_hz": float(np.mean(pd0)),
        "t0107_nd_at_180deg_mean_hz": float(np.mean(nd180)),
        "t0107_dsi_2dir_ratio_sanity_mean": float(np.mean(ratio)),
        "spearman_rho_t0106_vs_t0107_dsi": rho,
        "spearman_pvalue_t0106_vs_t0107_dsi": pval,
    }


def _build_details(
    *,
    metrics_at_creation: dict[str, float],
    instance_count: int,
) -> dict[str, object]:
    return {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": "8-direction polar recheck of 10 random top-50 t0106 cells",
        "short_description": (
            "Per-cell per-direction firing rates from re-evaluating 10 randomly chosen cells "
            "from the t0106 top-50 at an 8-direction stimulus protocol, together with "
            "recomputed vector-sum DSI and 2-direction ratio-DSI sanity check."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "DSGC compartmental models built from 68-dimensional joint Bed B electrophys + "
            "14-d morphology vectors using the t0092 fixed morphology generator with baseline "
            "channel insertion; AIS extension; AR(2)-noise driven moving-bar stimulus. The "
            "10 cells were selected from the 3,744 evaluations produced by the t0106 NSGA-II "
            "run (seed 44), deduplicated by (round(DSI, 4), round(PD, 2)), ranked by the "
            "joint-corner score `min(DSI/0.5, 1) * min(PD/30, 1)`, and sampled from the top "
            "50 with `numpy.random.default_rng(42)`."
        ),
        "dataset_ids": [],
        "prediction_format": "json",
        "prediction_schema": (
            "JSON object with fields `n_directions` (int = 8), `eval_seeds` (list[int] = "
            "[111, 222, 333]), `wall_clock_total_s` (float, total NEURON wall-clock), and "
            "`evaluations` (list[object]). Each evaluation has fields `t0106_rank` (int), "
            "`t0106_generation` (int), `t0106_dsi` (float, t0106 ratio-DSI), `t0106_pd_hz` "
            "(float, t0106 PD firing rate Hz), `vector_68d` (list[float], length 68), "
            "`angles_deg` (list[float], length 8, in [0, 45, 90, 135, 180, 225, 270, 315]), "
            "`per_direction_rates_hz` (list[float], length 8, mean firing rate over 3 noise "
            "seeds per direction), `t0107_dsi_8dir_vsum` (float, 8-direction vector-sum DSI), "
            "`t0107_pd_at_0deg` (float), `t0107_nd_at_180deg` (float), "
            "`t0107_dsi_2dir_ratio_sanity` (float)."
        ),
        "instance_count": instance_count,
        "metrics_at_creation": metrics_at_creation,
        "files": [
            {
                "path": "files/per_cell_polar_eval.json",
                "description": (
                    "Per-cell per-direction firing rates with original t0106 metrics and "
                    "recomputed t0107 vector-sum and ratio-DSI."
                ),
                "format": "json",
            }
        ],
        "categories": [
            "direction-selectivity",
            "compartmental-modeling",
            "retinal-ganglion-cell",
        ],
        "created_by_task": "t0107_t0106_polar_8dir_recheck",
        "date_created": DATE_CREATED,
    }


def _build_description(
    *,
    metrics: dict[str, float],
    cells: list[CellSummary],
) -> str:
    rho = metrics["spearman_rho_t0106_vs_t0107_dsi"]
    pval = metrics["spearman_pvalue_t0106_vs_t0107_dsi"]
    rows = [
        f"| {c.t0106_rank:>4} | {c.t0106_dsi:.3f} | {c.t0107_dsi_8dir_vsum:.3f} | "
        f"{c.t0107_pd_at_0deg:.1f} | {c.t0107_nd_at_180deg:.1f} | "
        f"{c.t0107_dsi_2dir_ratio_sanity:.3f} |"
        for c in sorted(cells, key=lambda c: c.t0106_rank)
    ]
    table = "\n".join(rows)
    return f"""---
spec_version: "2"
predictions_id: "{PREDICTIONS_ID}"
documented_by_task: "t0107_t0106_polar_8dir_recheck"
date_documented: "{DATE_CREATED}"
---

# 8-Direction Polar Recheck of 10 Random Top-50 t0106 Cells

## Metadata

* **Name**: 8-direction polar recheck of 10 random top-50 t0106 cells
* **Model**: DSGC compartmental cells from t0106 NSGA-II winners (68-d joint
  Bed B + morphology), no separate model asset
* **Datasets**: None (synthetic moving-bar stimulus generated by the t0107
  trial helpers)
* **Format**: json
* **Instances**: {int(metrics["n_cells"])} cells, 8 directions, 3 noise seeds
  = 240 NEURON simulations
* **Created by**: t0107_t0106_polar_8dir_recheck

## Overview

This predictions asset captures the 8-direction polar tuning curves for 10
cells selected at random from the top 50 cells of the t0106 long-NSGA-II
run. The t0106 winners were originally scored using a 2-direction (PD/ND)
ratio-DSI protocol, which is faster but cannot reveal whether the cell's
tuning curve has a single PD peak, a bimodal response, or an off-axis
preferred direction.

The t0107 protocol evaluates the same 68-d parameter vectors at 8
equally-spaced directions (0, 45, 90, 135, 180, 225, 270, 315 degrees) with
3 noise seeds per direction, then computes both the 8-direction vector-sum
DSI and a 2-direction ratio-DSI sanity check. The Spearman correlation
between the t0106 (2-direction) DSI and the t0107 (8-direction) DSI is
**rho = {rho:.3f}** (p = {pval:.3g}). The accompanying polar tuning-curve
plot in `results/images/polar_tuning_curves_top10.png` provides a visual
sanity check.

## Model

The model is the DSGC compartmental model defined by the t0106 evaluator
stack:

* 68-d joint parameter vector: 54-d Bed B electrophysiological parameters
  (channel densities, NMDA conductance, ACh/GABA synapse counts and weights)
  plus 14-d morphology parameters (primary branches, branching probability,
  Strahler depth, etc.)
* Morphology generated by `tasks.t0092_diagnose_morphology_generator_silence.
  code.morphology_generator_fix.generate_fixed_morphology` (canonical entry
  per correction C-0093-01)
* Baseline HHst + cad channels inserted via
  `tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels.
  insert_baseline_channels`
* Axon initial segment (AIS) extension and parametric synapse placement
  copied verbatim from t0106
* NEURON 8.2.7 with the t0080 mod library

The 10 cells were chosen from the 3,744 evaluations produced by the t0106
NSGA-II run (seed 44). The selection ranks them by the joint-corner score
`min(DSI/0.5, 1) * min(PD/30, 1)`, breaks ties by `dsi + pd/100`, takes the
top 50, and samples 10 deterministically with `numpy.random.default_rng(42)`.

## Data

There is no external evaluation dataset. The stimulus is a synthetic
moving-bar protocol generated by `code/trial_helpers.py`:

* 8 directions: 0, 45, 90, 135, 180, 225, 270, 315 degrees
* 3 noise replicates per direction (eval_seeds 111, 222, 333)
* Bar travel time and arrival profiles inherited from t0024 / t0080
* AR(2) noise model with `RHO_CORRELATED` correlation
* Simulation window: 1400 ms (TSTOP_MS)

Total NEURON simulations: 10 cells * 8 directions * 3 seeds = 240.

## Prediction Format

`files/per_cell_polar_eval.json` is a JSON object:

```text
{{
  "n_directions": 8,
  "eval_seeds": [111, 222, 333],
  "wall_clock_total_s": <float>,
  "evaluations": [
    {{
      "t0106_rank": <int>,
      "t0106_generation": <int>,
      "t0106_dsi": <float>,
      "t0106_pd_hz": <float>,
      "vector_68d": [<float> x 68],
      "angles_deg": [0, 45, 90, 135, 180, 225, 270, 315],
      "per_direction_rates_hz": [<float> x 8],
      "t0107_dsi_8dir_vsum": <float>,
      "t0107_pd_at_0deg": <float>,
      "t0107_nd_at_180deg": <float>,
      "t0107_dsi_2dir_ratio_sanity": <float>
    }},
    ...
  ]
}}
```

`per_direction_rates_hz[i]` is the mean firing rate across the 3 noise
seeds at angle `angles_deg[i]` (Hz, computed as mean spike count divided
by `TSTOP_MS / 1000.0`). The 2-direction ratio DSI is `(rate@0 - rate@180)
/ (rate@0 + rate@180)`, with 0 returned if the denominator is below 1e-12.
The 8-direction vector-sum DSI is `|sum_i(r_i * exp(i * theta_i))| /
sum_i(r_i)`.

## Metrics

Per-cell summary across the 10 cells:

| Rank | t0106 DSI | t0107 vsum-DSI | PD@0 (Hz) | ND@180 (Hz) | t0107 ratio-DSI |
| --- | --- | --- | --- | --- | --- |
{table}

| Aggregate | Value |
| --- | --- |
| n_cells | {int(metrics["n_cells"])} |
| t0107 vsum-DSI mean | **{metrics["t0107_dsi_8dir_vsum_mean"]:.3f}** |
| t0107 vsum-DSI std | {metrics["t0107_dsi_8dir_vsum_std"]:.3f} |
| t0107 vsum-DSI min | {metrics["t0107_dsi_8dir_vsum_min"]:.3f} |
| t0107 vsum-DSI max | {metrics["t0107_dsi_8dir_vsum_max"]:.3f} |
| PD@0 mean (Hz) | {metrics["t0107_pd_at_0deg_mean_hz"]:.2f} |
| ND@180 mean (Hz) | {metrics["t0107_nd_at_180deg_mean_hz"]:.2f} |
| t0107 ratio-DSI mean | {metrics["t0107_dsi_2dir_ratio_sanity_mean"]:.3f} |
| Spearman rho (t0106 vs t0107 DSI) | **{rho:.3f}** |
| Spearman p-value | {pval:.3g} |

## Main Ideas

* The 10 top-50 t0106 cells were re-evaluated at 8 stimulus directions to
  test whether their PD/ND advantage holds when probed off-axis. The
  Spearman rank correlation between t0106 (2-direction ratio-DSI) and
  t0107 (8-direction vector-sum DSI) is **rho = {rho:.3f}**.
* The 8-direction vector-sum DSI is always between 0 and 1 by construction
  and can be directly compared to published RGC tuning indices; the t0107
  mean vector-sum DSI across the 10 cells is
  **{metrics["t0107_dsi_8dir_vsum_mean"]:.3f}**.
* Mean firing rate at the preferred direction (0 deg) is
  **{metrics["t0107_pd_at_0deg_mean_hz"]:.2f} Hz** vs. null direction (180
  deg) **{metrics["t0107_nd_at_180deg_mean_hz"]:.2f} Hz**; the 2-direction
  ratio-DSI sanity check averages
  **{metrics["t0107_dsi_2dir_ratio_sanity_mean"]:.3f}**.
* Each cell's polar tuning curve is plotted in `results/images/
  polar_tuning_curves_top10.png` for visual inspection of shape (single
  peak vs. bimodal vs. off-axis preferred direction).

## Summary

This predictions asset records the 8-direction polar tuning curves for 10
cells randomly sampled from the top-50 of the t0106 long-NSGA-II run. The
t0106 evaluator used only 2 directions (PD = 0 deg, ND = 180 deg) and
reported a ratio-style DSI for speed; t0107 expands the evaluation to 8
directions with the same 68-d substrate, the same evaluator code base, and
the same DSI silence guard.

The Spearman rank correlation between the t0106 2-direction ratio-DSI and
the t0107 8-direction vector-sum DSI is **rho = {rho:.3f}** (p =
{pval:.3g}), with a t0107 mean vector-sum DSI of
**{metrics["t0107_dsi_8dir_vsum_mean"]:.3f}** across the 10 cells.
Per-direction firing rates and polar plots support downstream analyses
without re-running NEURON, and the asset directly tests whether the
2-direction simplification in t0106 captured the same direction-selective
behaviour as a denser 8-direction protocol.
"""


def main() -> None:
    cells = _load_summary(path=PER_CELL_POLAR_SOURCE)
    assert len(cells) == 10, f"expected 10 cells, got {len(cells)}"

    metrics = _compute_summary_metrics(cells=cells)
    instance_count = len(cells)

    FILES_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(PER_CELL_POLAR_SOURCE, PER_CELL_POLAR_DEST)

    details = _build_details(metrics_at_creation=metrics, instance_count=instance_count)
    DETAILS_JSON.write_text(
        json.dumps(details, indent=2) + "\n",
        encoding="utf-8",
    )

    description = _build_description(metrics=metrics, cells=cells)
    DESCRIPTION_MD.write_text(description, encoding="utf-8")

    print(f"Wrote {DETAILS_JSON}")
    print(f"Wrote {DESCRIPTION_MD}")
    print(f"Wrote {PER_CELL_POLAR_DEST}")
    print(f"  Built at {datetime.now(tz=UTC).isoformat()}")


if __name__ == "__main__":
    main()
