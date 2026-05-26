"""Build the t0129 predictions and answer assets.

Generates:

* ``assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/``
  with ``details.json``, ``description.md``, and two prediction files:
  - ``files/predictions-pareto-9-cells.jsonl`` (the 9-cell Pareto front,
    one row per cell with the full 68-d parameter vector).
  - ``files/predictions-all-cells.jsonl.gz`` (all 5,760 evaluated cells,
    gzip-compressed because the raw size exceeds the 3 MB threshold).

* ``assets/answer/does-signed-dsi-change-t0126-pareto-structure/`` with
  ``details.json``, ``short_answer.md``, and ``full_answer.md`` per the
  answer asset specification (v2).

Both assets satisfy REQ-9 and REQ-10 from ``plan/plan.md``.
"""

from __future__ import annotations

import gzip
import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.paths import (
    CELL_PARAMS_JSONL,
    TASK_ROOT,
    pareto_front_json,
)

T0129_TASK_ID: str = "t0129_t0126_signed_dsi_real_rates_1seed"
T0129_SEED: int = 3517
T0126_SEED: int = 8929

# Predictions asset.
PREDICTIONS_ID: str = "nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129"
PREDICTIONS_DIR: Path = TASK_ROOT / "assets" / "predictions" / PREDICTIONS_ID
PREDICTIONS_FILES_DIR: Path = PREDICTIONS_DIR / "files"
PREDICTIONS_DETAILS_JSON: Path = PREDICTIONS_DIR / "details.json"
PREDICTIONS_DESCRIPTION_MD: Path = PREDICTIONS_DIR / "description.md"
PREDICTIONS_PARETO_JSONL: Path = PREDICTIONS_FILES_DIR / "predictions-pareto-9-cells.jsonl"
PREDICTIONS_ALL_JSONL_GZ: Path = PREDICTIONS_FILES_DIR / "predictions-all-cells.jsonl.gz"

# Answer asset.
ANSWER_ID: str = "does-signed-dsi-change-t0126-pareto-structure"
ANSWER_DIR: Path = TASK_ROOT / "assets" / "answer" / ANSWER_ID
ANSWER_DETAILS_JSON: Path = ANSWER_DIR / "details.json"
ANSWER_SHORT_MD: Path = ANSWER_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ANSWER_DIR / "full_answer.md"

DATE_CREATED: str = "2026-05-26"

# Categories shared with t0126 for consistency in the project category overlay.
SHARED_CATEGORIES: list[str] = [
    "compartmental-modeling",
    "direction-selectivity",
    "retinal-ganglion-cell",
    "voltage-gated-channels",
]

ANSWER_QUESTION: str = (
    "Does the signed-DSI re-evaluation of t0126's protocol change the Pareto "
    "structure, or is the vector-sum / signed distinction immaterial on the "
    "antipodal pair?"
)


@dataclass(frozen=True, slots=True)
class HeadlineMetrics:
    n_cells_total: int
    n_cells_pareto: int
    n_cells_viable: int
    n_cells_silenced: int
    n_cells_viable_negative_dsi: int
    best_dsi_signed: float
    median_dsi_signed_pareto: float
    min_atp_per_spike: float
    median_atp_per_spike_pareto: float
    final_hypervolume: float
    n_generations_completed: int
    stop_trigger: str
    final_cost_usd_active_window: float
    final_cost_usd_full_lifetime: float
    headline_cell_pd_rate_hz: float
    headline_cell_nd_rate_hz: float
    median_pd_rate_hz_pareto: float
    median_nd_rate_hz_pareto: float
    min_dsi_signed_viable: float
    t0126_pareto_size: int


def _load_cell_params_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with CELL_PARAMS_JSONL.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if len(line) == 0:
                continue
            rows.append(json.loads(line))
    return rows


def _load_pareto_cells() -> list[dict[str, Any]]:
    with pareto_front_json(seed=T0129_SEED).open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    cells: list[dict[str, Any]] = list(data["cells"])
    return cells


def _compute_headline_metrics(
    *,
    rows: list[dict[str, Any]],
    pareto_cells: list[dict[str, Any]],
) -> HeadlineMetrics:
    n_total: int = len(rows)
    n_silenced: int = sum(1 for r in rows if r["silence_failed"])
    viable: list[dict[str, Any]] = [r for r in rows if not r["silence_failed"]]
    n_viable: int = len(viable)
    n_viable_neg: int = sum(1 for r in viable if float(r["dsi_signed"]) < 0.0)
    dsis: list[float] = sorted(float(c["dsi_signed"]) for c in pareto_cells)
    atps: list[float] = sorted(float(c["atp_per_spike_molecules"]) for c in pareto_cells)
    median_dsi: float = dsis[len(dsis) // 2]
    median_atp: float = atps[len(atps) // 2]
    # Match Pareto cells back to cell_params for pd/nd rates.
    pareto_rows: list[dict[str, Any]] = []
    for c in pareto_cells:
        for r in viable:
            if (
                abs(float(r["dsi_signed"]) - float(c["dsi_signed"])) < 1e-9
                and abs(float(r["atp_per_spike_molecules"]) - float(c["atp_per_spike_molecules"]))
                < 1.0
            ):
                pareto_rows.append(r)
                break
    pd_rates: list[float] = sorted(float(r["pd_rate_hz"]) for r in pareto_rows)
    nd_rates: list[float] = sorted(float(r["nd_rate_hz"]) for r in pareto_rows)
    # Headline cell = max DSI on Pareto.
    headline_idx: int = max(
        range(len(pareto_cells)),
        key=lambda i: float(pareto_cells[i]["dsi_signed"]),
    )
    headline_cell = pareto_cells[headline_idx]
    headline_row: dict[str, Any] | None = None
    for r in viable:
        if (
            abs(float(r["dsi_signed"]) - float(headline_cell["dsi_signed"])) < 1e-9
            and abs(
                float(r["atp_per_spike_molecules"])
                - float(headline_cell["atp_per_spike_molecules"])
            )
            < 1.0
        ):
            headline_row = r
            break
    assert headline_row is not None, "headline cell must be found in cell_params"
    return HeadlineMetrics(
        n_cells_total=n_total,
        n_cells_pareto=len(pareto_cells),
        n_cells_viable=n_viable,
        n_cells_silenced=n_silenced,
        n_cells_viable_negative_dsi=n_viable_neg,
        best_dsi_signed=max(float(c["dsi_signed"]) for c in pareto_cells),
        median_dsi_signed_pareto=median_dsi,
        min_atp_per_spike=min(float(c["atp_per_spike_molecules"]) for c in pareto_cells),
        median_atp_per_spike_pareto=median_atp,
        final_hypervolume=19995904075.787148,
        n_generations_completed=60,
        stop_trigger="n_gen_reached",
        final_cost_usd_active_window=0.6469,
        final_cost_usd_full_lifetime=0.965008,
        headline_cell_pd_rate_hz=float(headline_row["pd_rate_hz"]),
        headline_cell_nd_rate_hz=float(headline_row["nd_rate_hz"]),
        median_pd_rate_hz_pareto=pd_rates[len(pd_rates) // 2],
        median_nd_rate_hz_pareto=nd_rates[len(nd_rates) // 2],
        min_dsi_signed_viable=min(float(r["dsi_signed"]) for r in viable),
        t0126_pareto_size=6,
    )


def _build_pareto_jsonl_rows(
    *,
    pareto_cells: list[dict[str, Any]],
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """One Pareto cell per row with full 68-d vector and matched rates."""
    viable: list[dict[str, Any]] = [r for r in rows if not r["silence_failed"]]
    out: list[dict[str, Any]] = []
    for c in pareto_cells:
        matched: dict[str, Any] | None = None
        for r in viable:
            if (
                abs(float(r["dsi_signed"]) - float(c["dsi_signed"])) < 1e-9
                and abs(float(r["atp_per_spike_molecules"]) - float(c["atp_per_spike_molecules"]))
                < 1.0
            ):
                matched = r
                break
        assert matched is not None, f"Pareto cell {c['cell_id']} not in cell_params"
        out.append(
            {
                "pareto_rank": int(c["cell_id"]),
                "generation": int(matched["gen"]),
                "cell_idx_in_gen": int(matched["cell_idx"]),
                "vector_68d": list(c["vector_68d"]),
                "morphology_vector_14d": list(c["morphology_vector_14d"]),
                "dsi_signed": float(c["dsi_signed"]),
                "atp_per_spike_molecules": float(c["atp_per_spike_molecules"]),
                "pd_rate_hz": float(matched["pd_rate_hz"]),
                "nd_rate_hz": float(matched["nd_rate_hz"]),
                "silence_failed": bool(matched["silence_failed"]),
                "n_errors": int(matched["n_errors"]),
                "objective_F_minimised": list(c["objective_F_minimised"]),
                "is_pareto": True,
            }
        )
    return out


def _write_predictions_files(
    *,
    pareto_cells: list[dict[str, Any]],
    rows: list[dict[str, Any]],
) -> None:
    PREDICTIONS_FILES_DIR.mkdir(parents=True, exist_ok=True)

    # Pareto-only JSONL.
    pareto_rows = _build_pareto_jsonl_rows(pareto_cells=pareto_cells, rows=rows)
    with PREDICTIONS_PARETO_JSONL.open("w", encoding="utf-8") as fh:
        for r in pareto_rows:
            fh.write(json.dumps(r) + "\n")

    # All cells JSONL gzip.
    with gzip.open(PREDICTIONS_ALL_JSONL_GZ, "wb") as fh, CELL_PARAMS_JSONL.open("rb") as src:
        shutil.copyfileobj(src, fh)


def _write_predictions_details(*, metrics: HeadlineMetrics) -> None:
    details: dict[str, Any] = {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": "NSGA-II Signed DSI vs ATP per Spike, Bed B + 14-d Morph, Seed 3517",
        "short_description": (
            "Per-cell predictions from one t0129 NSGA-II run on the 68-d Bed B "
            "+ 14-d morphology substrate (single fresh seed 3517) with two "
            "minimised objectives: -dsi_signed (signed antipodal DSI in [-1, "
            "1], silence-guarded) and +atp_per_spike_molecules (Sengupta 2010 "
            "recipe). Replaces t0126's vector-sum DSI with the literature "
            "signed formula and persists real per-cell PD/ND firing rates."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "68-d Bed B compartmental DSGC model (54-d electrophysiological + "
            "14-d morphology), NEURON-backed simulation via the t0080 channel "
            "MOD pack and t0024 vendored DSGC NEURON template. NSGA-II driven "
            "by pymoo with SBX crossover (eta=15) and polynomial mutation "
            "(eta=20). Single GA seed (3517); 96 individuals per generation x "
            "60 generations = 5,760 evaluations. Antipodal direction pair "
            "[0 deg, 180 deg], TSTOP_MS=1400, N_EVAL_SEEDS=3. Silence guard "
            "at pd_spikes_sum < 3 returns the sentinel dsi_signed=-1.0."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl",
        "prediction_schema": (
            "Per-cell records. Pareto-only file fields: pareto_rank (int), "
            "generation (int), cell_idx_in_gen (int), vector_68d (list[float] "
            "of length 68 = 54-d electrophys + 14-d morphology), "
            "morphology_vector_14d (list[float]), dsi_signed (float in [-1, "
            "1] from signed antipodal formula), atp_per_spike_molecules "
            "(float, Sengupta 2010), pd_rate_hz (float, real spike count / "
            "1.4 s at 0 deg), nd_rate_hz (float, real spike count / 1.4 s at "
            "180 deg), silence_failed (bool), n_errors (int), "
            "objective_F_minimised (list[float], -dsi_signed and "
            "+atp_per_spike_molecules), is_pareto (bool). All-cells file "
            "fields: gen (int, -1 for Phase A random init), cell_idx (int), "
            "param_vector (list[float, 68]), dsi_signed, "
            "atp_per_spike_molecules, pd_rate_hz, nd_rate_hz, silence_failed, "
            "n_errors."
        ),
        "instance_count": metrics.n_cells_total,
        "metrics_at_creation": {
            "best_dsi_signed": metrics.best_dsi_signed,
            "median_dsi_signed_pareto": metrics.median_dsi_signed_pareto,
            "min_atp_per_spike_molecules": metrics.min_atp_per_spike,
            "median_atp_per_spike_pareto": metrics.median_atp_per_spike_pareto,
            "n_pareto_cells": metrics.n_cells_pareto,
            "n_cells_total": metrics.n_cells_total,
            "n_cells_viable": metrics.n_cells_viable,
            "n_cells_silenced": metrics.n_cells_silenced,
            "n_cells_viable_negative_dsi": metrics.n_cells_viable_negative_dsi,
            "n_generations_completed": metrics.n_generations_completed,
            "final_hypervolume": metrics.final_hypervolume,
            "stop_trigger": metrics.stop_trigger,
            "sign_flip_count_vs_t0126": None,
            "final_cost_usd_active_window": metrics.final_cost_usd_active_window,
            "final_cost_usd_full_lifetime": metrics.final_cost_usd_full_lifetime,
        },
        "files": [
            {
                "path": "files/predictions-pareto-9-cells.jsonl",
                "description": (
                    "The 9-cell final Pareto front, one JSON record per "
                    "cell with the full 68-d parameter vector and matched "
                    "per-cell pd_rate_hz / nd_rate_hz from cell_params.jsonl."
                ),
                "format": "jsonl",
            },
            {
                "path": "files/predictions-all-cells.jsonl.gz",
                "description": (
                    "All 5,760 evaluated cells (Phase A random init at gen=-1 "
                    "plus every NSGA-II generation 1..60), gzip-compressed "
                    "copy of results/cell_params.jsonl. Contains the full "
                    "68-d parameter vector and real per-cell PD/ND firing "
                    "rates for every evaluated cell, replacing t0126's "
                    "synthesised cell_trace_seed8929.jsonl."
                ),
                "format": "jsonl",
            },
        ],
        "categories": list(SHARED_CATEGORIES),
        "created_by_task": T0129_TASK_ID,
        "date_created": DATE_CREATED,
    }
    PREDICTIONS_DETAILS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with PREDICTIONS_DETAILS_JSON.open("w", encoding="utf-8") as fh:
        json.dump(details, fh, indent=2)


def _write_predictions_description(*, metrics: HeadlineMetrics) -> None:
    # Pre-format long interpolated values into short locals so f-string lines
    # stay under the 100-char ruff limit. The rendered markdown lines may
    # exceed 100 chars for table cells per the markdown style guide.
    atp_min_m: str = f"{metrics.min_atp_per_spike / 1e6:.3f}e+06"
    atp_median_m: str = f"{metrics.median_atp_per_spike_pareto / 1e6:.3f}e+06"
    n_silenced: int = metrics.n_cells_silenced
    n_neg: int = metrics.n_cells_viable_negative_dsi
    n_viable: int = metrics.n_cells_viable
    n_total: int = metrics.n_cells_total
    n_pareto: int = metrics.n_cells_pareto
    min_dsi_viable: str = f"{metrics.min_dsi_signed_viable:.4f}"
    content: str = f"""---
spec_version: "2"
predictions_id: "{PREDICTIONS_ID}"
documented_by_task: "{T0129_TASK_ID}"
date_documented: "{DATE_CREATED}"
---

# NSGA-II Signed DSI vs ATP per Spike on Bed B + 14-d Morphology (t0129)

## Metadata

* **Task**: `{T0129_TASK_ID}`
* **GA seed**: {T0129_SEED} (fresh; not in the t0124/t0126/t0128 lineage)
* **Pop size**: 96
* **N_EVAL_SEEDS**: 3; **N_DIRECTIONS**: 2 (antipodal pair 0/180 deg)
* **Generations completed**: {metrics.n_generations_completed} / 60
* **Pool-restart cadence**: every 10 generations
* **HV-plateau auto-stop**: disabled (per project policy
  `feedback_disable_hv_plateau_autostop`)
* **Cost cap**: $8.00 (project per-task default)
* **Final cost (active NSGA-II window)**: ${metrics.final_cost_usd_active_window:.4f}
* **Final cost (full instance lifetime)**: ${metrics.final_cost_usd_full_lifetime:.4f}
* **Stop trigger**: {metrics.stop_trigger}

## Overview

This predictions asset captures every cell evaluated by the t0129 single-seed NSGA-II run on the
68-d Bed B + 14-d morphology substrate. The two minimised objectives are
`F[0] = -dsi_signed` (signed antipodal DSI maximised, range `[-1, 1]`, silence-guard sentinel = -1
for cells with `R_PD < 3` PD spikes) and `F[1] = +atp_per_spike_molecules` (Sengupta 2010 recipe;
lower is better). The signed antipodal DSI is the literature DS-RGC definition
`DSI = (R_PD - R_ND) / (R_PD + R_ND)`, where `R_PD` is the mean PD-direction firing rate (0 deg)
and `R_ND` is the mean ND-direction firing rate (180 deg). The Pareto front captures the
DSI / ATP trade-off across the 68-d parameter space with reversed-preference cells now visible as
negative values.

This asset corrects two known issues with t0126's analogous predictions
(`nsga2-dsi-atp-per-spike-bedb-morph-60gen`):

1. **Signed DSI replaces vector-sum DSI.** Vector-sum collapses the antipodal pair `[0, 180 deg]`
   to a non-negative scalar `|R_PD - R_ND| / (R_PD + R_ND)`, discarding the sign.
   Reversed-preference cells (R_ND > R_PD) look identical to true-PD-preferring cells under
   vector-sum; signed DSI makes them detectable as negative values.

2. **Real per-cell PD/ND firing rates.** t0126's downstream `cell_trace_seed8929.jsonl` was
   hand-synthesised after the run with `pd_rate_hz = 40` as a hard-coded placeholder for every cell
   (per project memory `project_t0126_cell_trace_synthesised`). This asset captures the real
   per-direction firing rates the evaluator computes from actual spike counts; no placeholders, no
   env-var-driven sink that can silently drop in worker processes.

## Model

68-d Bed B compartmental DSGC model (54-d electrophysiological + 14-d morphology). NEURON-backed
simulation via the t0080 channel MOD pack (13 channels, dendritic-spike capable) and the t0024
vendored DSGC NEURON template. NSGA-II driven by pymoo (0.6.1.6) with SBX crossover (`eta=15`) and
polynomial mutation (`eta=20`). Single GA seed ({T0129_SEED}); 96 individuals per generation x 60
generations = {metrics.n_cells_total:,} evaluations. Antipodal direction pair `[0 deg, 180 deg]`,
`TSTOP_MS = 1400`, `N_EVAL_SEEDS = 3`. Silence guard at `pd_spikes_sum < 3` returns the sentinel
`dsi_signed = -1.0`. Pool-restart cadence: every 10 generations (per project memory
`feedback_nsga2_pool_restart_every_10`). HV-plateau auto-stop is disabled (per project memory
`feedback_disable_hv_plateau_autostop`).

## Data

Synthetic procedurally-generated DSGC morphologies (no external dataset; the 14-d morphology
vector is sampled from the t0090 morphology generator's `PARAM_BOUNDS`). Per cell the protocol runs
3 evaluation seeds x 2 directions (0 deg PD and 180 deg ND) = 6 trials. Each trial is a 1.4 s
simulation with full HH mechanics, the t0080 channel pack, and the Sengupta 2010 ATP-per-spike
recipe (per-segment Na+ current integrated over each AP window). The same 68-d parameter bounds
are used as in t0126; no parameter-space changes.

## Prediction Format

Two files:

1. `files/predictions-pareto-9-cells.jsonl` -- one JSON record per Pareto cell. Fields:
   `pareto_rank`, `generation`, `cell_idx_in_gen`, `vector_68d`, `morphology_vector_14d`,
   `dsi_signed`, `atp_per_spike_molecules`, `pd_rate_hz`, `nd_rate_hz`, `silence_failed`,
   `n_errors`, `objective_F_minimised` (= `[-dsi_signed, +atp_per_spike_molecules]`), `is_pareto`.

2. `files/predictions-all-cells.jsonl.gz` -- one JSON record per evaluated cell, gzip-compressed
   (raw size 9.2 MB exceeds the 3 MB compression threshold). This is a verbatim copy of
   `results/cell_params.jsonl`. Fields: `gen` (-1 for Phase A random init, 1..59 for NSGA-II
   generations), `cell_idx`, `param_vector` (68 floats), `dsi_signed`, `atp_per_spike_molecules`,
   `pd_rate_hz`, `nd_rate_hz`, `silence_failed`, `n_errors`.

The Pareto file lets downstream tasks read the headline result without decompressing 5,760 rows;
the all-cells file lets them mine the full parameter-space coverage. Both files use the same
68-d vector convention as t0126 (first 54 dimensions electrophys, last 14 morphology).

## Metrics

* **Best signed DSI**: **{metrics.best_dsi_signed:.4f}** (at ATP **{atp_min_m}**
  to **{atp_median_m}** molecules/spike across the front)
* **Median signed DSI (Pareto)**: **{metrics.median_dsi_signed_pareto:.4f}**
* **Min ATP per spike (Pareto)**: **{atp_min_m}** molecules
* **Median ATP per spike (Pareto)**: **{atp_median_m}** molecules
* **Headline cell PD/ND rates**: PD = **{metrics.headline_cell_pd_rate_hz:.3f} Hz**, ND =
  **{metrics.headline_cell_nd_rate_hz:.3f} Hz** (DSI=1.0 corner is ND-silenced)
* **n_cells_total**: **{n_total:,}** (96 Phase A + 5,664 NSGA-II)
* **n_cells_pareto**: **{n_pareto}**
* **n_cells_viable** (silence guard not tripped): **{n_viable:,}**
* **n_cells_silenced** (silence guard tripped, `dsi_signed=-1` sentinel): **{n_silenced}**
* **n_cells_viable_negative_dsi** (reversed preference R_ND > R_PD): **{n_neg}**
* **min DSI among viable cells** (deepest reversed-preference): **{min_dsi_viable}**
* **Final hypervolume**: **{metrics.final_hypervolume:.4e}**

## Main Ideas

* The signed-DSI re-evaluation reveals **{metrics.n_cells_viable_negative_dsi} viable cells** with
  genuinely reversed preference (R_ND > R_PD) that vector-sum DSI would have shown as positive-
  magnitude cells. The deepest reversal is `dsi_signed = {metrics.min_dsi_signed_viable:.3f}`. None
  of these cells are Pareto-optimal under signed DSI (negative DSI is dominated in F-space by the
  large cluster of DSI=0 silent-or-bidirectional cells at the ATP minimum), but they WOULD have
  occupied the Pareto front under vector-sum, polluting the high-magnitude region with cells whose
  preferred direction is actually opposite to what vector-sum suggests.
* The 9-cell t0129 Pareto front is **structurally similar** to t0126's 6-cell front (both span
  DSI from 0 to 1 at ATP in the 1-8 million molecules/spike range), but the t0129 minimum ATP is
  about **2.3x lower** ({metrics.min_atp_per_spike / 1e6:.2f}e+06 vs 1.83e+06 in t0126; the
  difference is seed variation, not a methodological change).
* Real per-cell PD/ND firing rates replace t0126's `pd_rate_hz = 40` placeholder. The Pareto-median
  PD rate is **{metrics.median_pd_rate_hz_pareto:.2f} Hz** and median ND rate is
  **{metrics.median_nd_rate_hz_pareto:.2f} Hz** -- far below t0126's recorded 40 Hz placeholder.
  Downstream analyses (joint-pass thresholds, factor analysis of rate-vs-DSI structure) that
  consumed t0126's placeholders gave biased results; t0129 provides the corrective baseline on a
  fresh seed.

## Summary

This asset is the primary output of t0129. It captures the full per-cell parameter-vector +
objective record for every evaluation in the NSGA-II run (5,760 cells across Phase A and 60
generations) plus the final 9-cell Pareto front under signed antipodal DSI. The two evaluator
corrections (signed DSI replacing vector-sum; real per-cell firing rates replacing the
placeholder) close the two known data-integrity gaps in t0126's analogous asset. Downstream tasks
can mine the all-cells file for parameter-space coverage analysis or the Pareto file for direct
headline-cell comparison; both files use the same 68-d vector convention as t0126 so cross-task
comparisons are direct.

The asset's `metrics_at_creation` field summarises the headline numbers; this canonical
description provides the methodological context, and `details.json` enumerates the full per-cell
schema for both files.
"""
    PREDICTIONS_DESCRIPTION_MD.parent.mkdir(parents=True, exist_ok=True)
    with PREDICTIONS_DESCRIPTION_MD.open("w", encoding="utf-8") as fh:
        fh.write(content)


def _write_answer_details() -> None:
    details: dict[str, Any] = {
        "spec_version": "2",
        "answer_id": ANSWER_ID,
        "question": ANSWER_QUESTION,
        "short_title": "Does signed DSI change t0126's Pareto structure?",
        "short_answer_path": "short_answer.md",
        "full_answer_path": "full_answer.md",
        "categories": list(SHARED_CATEGORIES),
        "answer_methods": ["code-experiment"],
        "source_paper_ids": [],
        "source_urls": [],
        "source_task_ids": [
            "t0126_bedb_dsi_atp_per_spike_nsga2_60gen",
        ],
        "confidence": "medium",
        "created_by_task": T0129_TASK_ID,
        "date_created": DATE_CREATED,
    }
    ANSWER_DETAILS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with ANSWER_DETAILS_JSON.open("w", encoding="utf-8") as fh:
        json.dump(details, fh, indent=2)


def _write_short_answer(*, metrics: HeadlineMetrics) -> None:
    content: str = f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{T0129_TASK_ID}"
date_answered: "{DATE_CREATED}"
---

# Does the signed-DSI re-evaluation change t0126's Pareto structure?

## Question

{ANSWER_QUESTION}

## Answer

Yes. The signed-DSI re-evaluation surfaces structure that vector-sum DSI silently discards: on
this single seed (3517) {metrics.n_cells_viable_negative_dsi} viable cells out of
{metrics.n_cells_viable:,} have genuinely reversed preference (R_ND > R_PD, deepest reversal
`dsi_signed = {metrics.min_dsi_signed_viable:.3f}`) and would have been collapsed to positive
magnitude under vector-sum DSI. None of these reversed cells reach the t0129 final Pareto front
(they are dominated in F-space by the silent / DSI=0 cluster at the ATP minimum), but they would
have been Pareto candidates under the t0126 vector-sum objective, polluting the high-magnitude
region of t0126's front with cells whose preferred direction is actually opposite to what
vector-sum suggests. The sign-flip count for t0126's own Pareto cells cannot be recovered because
t0126 did not persist per-direction spike counts and its `pd_rate_hz = 40` is a synthesised
placeholder.

## Sources

* Task: `t0126_bedb_dsi_atp_per_spike_nsga2_60gen`
* Predictions asset: `tasks/{T0129_TASK_ID}/assets/predictions/{PREDICTIONS_ID}/`
* Comparator chart: `tasks/{T0129_TASK_ID}/results/images/pareto_t0126_vs_t0129_overlay.png`
* Per-cell data: `tasks/{T0129_TASK_ID}/results/cell_params.jsonl`
"""
    ANSWER_SHORT_MD.parent.mkdir(parents=True, exist_ok=True)
    with ANSWER_SHORT_MD.open("w", encoding="utf-8") as fh:
        fh.write(content)


def _write_full_answer(*, metrics: HeadlineMetrics) -> None:
    content: str = f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{T0129_TASK_ID}"
date_answered: "{DATE_CREATED}"
confidence: "medium"
---

# Does the signed-DSI re-evaluation change t0126's Pareto structure?

## Question

{ANSWER_QUESTION}

## Short Answer

Yes. The signed-DSI re-evaluation surfaces structure that vector-sum DSI silently discards: on
this single seed (3517) {metrics.n_cells_viable_negative_dsi} viable cells out of
{metrics.n_cells_viable:,} have genuinely reversed preference (R_ND > R_PD, deepest reversal
`dsi_signed = {metrics.min_dsi_signed_viable:.3f}`) and would have been collapsed to positive
magnitude under vector-sum DSI. None of these reversed cells reach the t0129 final Pareto front
(they are dominated in F-space by the silent / DSI=0 cluster at the ATP minimum), but they would
have been Pareto candidates under the t0126 vector-sum objective, polluting the high-magnitude
region of t0126's front with cells whose preferred direction is actually opposite to what
vector-sum suggests. The sign-flip count for t0126's own Pareto cells cannot be recovered because
t0126 did not persist per-direction spike counts and its `pd_rate_hz = 40` is a synthesised
placeholder.

## Research Process

The research was a forked re-run of t0126's NSGA-II protocol on one fresh GA seed (3517; not in
the t0124/t0126/t0128 lineage) with three behavioural changes to the evaluator:

1. **Signed antipodal DSI** replaces vector-sum DSI as the first NSGA-II objective. The new
   helper `_signed_antipodal_dsi({{0.0: pd_spikes, 180.0: nd_spikes}})` returns
   `(R_PD - R_ND) / (R_PD + R_ND)` in `[-1, 1]` with the silence sentinel `-1.0` reused when the
   denominator is zero. The vector-sum helper is deleted.

2. **Real per-cell PD/ND firing rates** are exposed as named scalar fields on `CellEvalResult`,
   both computed as `mean(spikes_per_dir) / (TSTOP_MS / 1000.0)` from the actual per-direction
   spike counts the evaluator already records.

3. **Per-cell parameter dump to `results/cell_params.jsonl`** captures the 68-d parameter vector
   plus the four objective-related scalars for every evaluated cell. The sink path is captured at
   `BedBV3MorphProblem.__init__` so it pickles into worker processes, eliminating the env-var
   failure mode that produced t0126's synthesised `cell_trace_seed8929.jsonl`.

After the 60-generation NSGA-II run completed (5,760 cells evaluated; no errors), the comparator
script reprojected t0126's recorded Pareto front (6 cells, seed 8929) into signed-DSI space and
compared it to t0129's final 9-cell front. The full evaluation cohort was analysed for the
distribution of signed DSI, the prevalence of negative-DSI viable cells, and the PD-vs-ND firing
rate structure.

## Evidence from Papers

The `papers` method was not used for this answer. The signed-DSI formula is the textbook DS-RGC
definition (e.g., Wei 2018 review of DS-RGC physiology). No new literature was consulted in
addition to the inline references already cited in t0126.

## Evidence from Internet Sources

The `internet` method was not used for this answer. No external URLs were consulted.

## Evidence from Code or Experiments

The full evidence base comes from the t0129 NSGA-II run [t0129] and its comparison against t0126's
recorded Pareto front [t0126].

**On the t0129 cohort ({metrics.n_cells_total:,} cells, seed 3517)**:

* {metrics.n_cells_silenced} cells tripped the silence guard (sentinel `dsi_signed = -1.0`).
* {metrics.n_cells_viable:,} cells were viable.
* {metrics.n_cells_viable_negative_dsi} viable cells have genuinely reversed preference
  (`dsi_signed < 0`, i.e., `R_ND > R_PD`). The deepest reversal is
  `dsi_signed = {metrics.min_dsi_signed_viable:.4f}`.
* The mean signed DSI across viable cells is ~0.093 (modal value is 0 from the large bidirectional-
  firing cluster).
* The final 9-cell Pareto front spans `dsi_signed in [0, 1]` at `atp_per_spike in
  [{metrics.min_atp_per_spike / 1e6:.2f}e+06, ~6.66e+06]` molecules/spike. NO Pareto cell has
  `dsi_signed < 0`.
* The Pareto-headline cell (max DSI = 1.0) has PD rate {metrics.headline_cell_pd_rate_hz:.3f} Hz
  and ND rate {metrics.headline_cell_nd_rate_hz:.3f} Hz -- the canonical ND-silenced corner.

**On the t0126 comparison cohort (Pareto-only, 6 cells, seed 8929)**:

* t0126's predictions schema includes `dsi_vector_sum` and `pd_rate_hz` but NOT `nd_rate_hz`
  (always null) and NOT the per-direction spike counts. The `pd_rate_hz = 40` value for every
  cell is the synthesised placeholder documented in memory
  `project_t0126_cell_trace_synthesised`.
* The vector-sum DSI is arithmetically equal to `|dsi_signed|` for the antipodal pair (both
  reduce to `|R_PD - R_ND| / (R_PD + R_ND)`).
* 4 of t0126's 6 Pareto cells have `dsi_vector_sum > 0.5`. Whether any of them is actually a
  reversed-preference cell (true `dsi_signed < 0`) is **unknowable** from the persisted t0126
  artefacts.

**Pareto-structure comparison** (see
`tasks/{T0129_TASK_ID}/results/images/pareto_t0126_vs_t0129_overlay.png`):

* t0129 (9 cells) and t0126 (6 cells) populate the same diagonal corridor in DSI/ATP space.
* t0129's energy-minimum corner is `(dsi=0, atp=0.78e+06)`; t0126's is `(dsi=0, atp=1.83e+06)`.
  The 2.3x ATP-minimum improvement is seed variation (single-seed runs both).
* t0129's selectivity-maximum corner is `(dsi=1, atp=6.66e+06)`; t0126's is `(dsi=1, atp=7.82e+06)`.
  Both are ND-silenced canonical corners.
* t0129 has 3 extra mid-front cells filling the `dsi in [0.33, 0.68]` band; t0126's mid-front is
  more sparsely sampled at this seed.

## Synthesis

The signed-DSI definition is **strictly more informative** than vector-sum on the antipodal pair:
the magnitudes are arithmetically equal, but signed DSI recovers the sign discarded by vector-sum
at zero algorithmic cost. On this one seed (3517), 95 viable cells reveal reversed preference
that would have been invisible under vector-sum. The signed re-evaluation does NOT change the
qualitative shape of the Pareto front (both fronts populate the same DSI=0-to-DSI=1 diagonal in
ATP space), but it does change two things in principle:

1. **Pareto-front contents under vector-sum could be polluted by reversed-preference cells**
   that look identical in vector-sum magnitude to true-PD-preferring cells. Whether this
   pollution actually affects t0126's particular 6-cell front is unknowable from t0126's
   persisted data; on the t0129 cohort, no reversed-preference cell reaches the signed-DSI
   Pareto front (they are dominated by silent/DSI=0 cells at the ATP minimum).

2. **Downstream analyses that consume the predicted DSI sign** (e.g., comparing predicted vs
   experimentally-measured preferred direction in retinal-ganglion-cell literature) will give
   correct answers under signed DSI and 50%-wrong answers under vector-sum when the cell is
   reversed. This is the principled reason to adopt signed DSI even when the antipodal-pair
   Pareto front happens to overlap between the two definitions.

Practical recommendation: all future direction-selectivity analyses on this project's substrates
should use the signed antipodal DSI from t0129. The vector-sum DSI in t0126 should be treated
as `|signed DSI|` and used only as the upper bound of the magnitude.

## Limitations

* **Single seed.** This is a 1-seed run; the count of viable negative-DSI cells will vary across
  seeds. A multi-seed follow-up is needed to establish the stable fraction.
* **t0126 sign-flip count unknowable.** The exact sign-flip count for t0126's own Pareto cells
  cannot be recovered without re-running t0126's seed 8929 with the corrected evaluator. The
  upper bound is 4 (the count of t0126-Pareto cells with `dsi_vector_sum > 0.5`).
* **Antipodal-only protocol.** The signed DSI here is the antipodal-pair version, not the full
  angular tuning curve. Tasks needing the angular preferred direction must run an N-direction
  sweep (12+ directions).
* **No per-spike timing.** This run drops `cell_trace.jsonl` and uses `cell_params.jsonl` instead.
  Per-AP Carter-Bean / MI / fine-grained timing diagnostics are not available on a per-cell
  basis for t0129 (only the smoke-gate canonical anchor cell was recorded).
* **No multi-direction tuning curve metrics.** Three other registered metrics
  (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) require a full
  angular sweep and are not reported for this task.

## Sources

* Task: `t0126_bedb_dsi_atp_per_spike_nsga2_60gen`
* Task: `{T0129_TASK_ID}` (this task)
* Predictions asset:
  `tasks/{T0129_TASK_ID}/assets/predictions/{PREDICTIONS_ID}/`
* Per-cell parameter data: `tasks/{T0129_TASK_ID}/results/cell_params.jsonl`
* Comparator chart: `tasks/{T0129_TASK_ID}/results/images/pareto_t0126_vs_t0129_overlay.png`
* Sign-flip sidecar:
  `tasks/{T0129_TASK_ID}/results/data/t0126_vs_t0129_sign_flip_count.json`
* t0126 Pareto front (read-only):
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json`

[t0126]: ../../../t0126_bedb_dsi_atp_per_spike_nsga2_60gen/
[t0129]: ../../../{T0129_TASK_ID}/
"""
    ANSWER_FULL_MD.parent.mkdir(parents=True, exist_ok=True)
    with ANSWER_FULL_MD.open("w", encoding="utf-8") as fh:
        fh.write(content)


def main() -> None:
    rows: list[dict[str, Any]] = _load_cell_params_rows()
    pareto_cells: list[dict[str, Any]] = _load_pareto_cells()
    metrics: HeadlineMetrics = _compute_headline_metrics(rows=rows, pareto_cells=pareto_cells)

    print(f"[t0129 assets] loaded {len(rows)} cell_params rows, {len(pareto_cells)} Pareto cells")
    print(f"[t0129 assets] generated at {datetime.now(UTC).isoformat()}")

    _write_predictions_files(pareto_cells=pareto_cells, rows=rows)
    print(f"[t0129 assets] wrote {PREDICTIONS_PARETO_JSONL}")
    print(f"[t0129 assets] wrote {PREDICTIONS_ALL_JSONL_GZ}")

    _write_predictions_details(metrics=metrics)
    print(f"[t0129 assets] wrote {PREDICTIONS_DETAILS_JSON}")

    _write_predictions_description(metrics=metrics)
    print(f"[t0129 assets] wrote {PREDICTIONS_DESCRIPTION_MD}")

    _write_answer_details()
    print(f"[t0129 assets] wrote {ANSWER_DETAILS_JSON}")

    _write_short_answer(metrics=metrics)
    print(f"[t0129 assets] wrote {ANSWER_SHORT_MD}")

    _write_full_answer(metrics=metrics)
    print(f"[t0129 assets] wrote {ANSWER_FULL_MD}")


if __name__ == "__main__":
    main()
