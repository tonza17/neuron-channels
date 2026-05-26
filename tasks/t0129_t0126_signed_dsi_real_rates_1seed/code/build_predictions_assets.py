"""Build the t0123 predictions asset (REQ-24).

Creates ``tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/predictions/
nsga2-mi-atp-per-spike-bedb-morph/`` with:

* ``details.json`` per ``meta/asset_types/predictions/specification.md``
  (spec_version "2", prediction_format "jsonl.gz", per-cell schema
  describing the 68-d vector + MI + ATP/spike + per-compartment ATP
  breakdown + per-direction firing + DSI / PD-rate diagnostics +
  silence-failed / legit booleans).
* ``description.md`` -- the canonical documentation document.
* ``files/predictions.jsonl.gz`` -- every per-cell row from the
  per-cell side-channel trace + ``all_evaluations_seed<S>.json`` as
  gzipped JSONL. The 10 cells re-evaluated under the post-hoc
  Strong-Bialek protocol carry the extra
  ``mi_strong_bialek_bits_per_sec``, ``std_err_bits_per_sec``, and
  ``r_squared`` fields.
"""

from __future__ import annotations

import argparse
import gzip
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.constants import T0129_SEEDS
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.paths import (
    RESULTS_DATA_DIR,
    TASK_ROOT,
)

PREDICTIONS_ID: str = "nsga2-mi-atp-per-spike-bedb-morph"
ASSET_DIR: Path = TASK_ROOT / "assets" / "predictions" / PREDICTIONS_ID
DETAILS_PATH: Path = ASSET_DIR / "details.json"
DESCRIPTION_PATH: Path = ASSET_DIR / "description.md"
FILES_DIR: Path = ASSET_DIR / "files"
PREDICTIONS_JSONL_GZ: Path = FILES_DIR / "predictions.jsonl.gz"

# LEGIT cohort definition: DSI >= 0.5 (tracked diagnostic), PD-rate
# >= 30 Hz, NOT silence-failed.
LEGIT_DSI_THRESHOLD: float = 0.5
LEGIT_PD_RATE_HZ_THRESHOLD: float = 30.0


def _load_all_evaluations(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"all_evaluations_seed{seed}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("evaluations", []))


def _load_cell_trace_jsonl(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"cell_trace_seed{seed}.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _load_pareto(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("cells", []))


def _load_hv_trajectory(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"hv_trajectory_seed{seed}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("trajectory", [])


def _load_strong_bialek_top10() -> dict[str, dict[str, Any]]:
    """Return a {cell_index_int: row_dict} map for post-hoc cells."""
    path = RESULTS_DATA_DIR / "post_hoc_strong_bialek_mi_top10.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict[str, Any]] = {}
    for entry in payload.get("cells", []):
        key = str(entry.get("cell_index"))
        out[key] = entry
    return out


def _is_legit(*, row: dict[str, Any]) -> bool:
    dsi = float(row.get("dsi_vector_sum", 0.0))
    pd_rate = float(row.get("pd_rate_hz", 0.0))
    silence_failed = bool(row.get("silence_failed", False))
    return (
        dsi >= LEGIT_DSI_THRESHOLD and pd_rate >= LEGIT_PD_RATE_HZ_THRESHOLD and not silence_failed
    )


def _merge_rows(
    *,
    trace_rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
    strong_bialek_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build per-cell rows from the cell trace if present, otherwise from
    the all_evaluations payload. Augment Pareto cells (top-10) with
    Strong-Bialek bits/s when available.
    """
    out: list[dict[str, Any]] = []
    if len(trace_rows) > 0:
        for idx, row in enumerate(trace_rows):
            merged = dict(row)
            merged.setdefault("cell_index", idx)
            merged["legit_bool"] = _is_legit(row=merged)
            key = str(merged.get("cell_index"))
            sb = strong_bialek_map.get(key)
            if sb is not None:
                merged["mi_strong_bialek_bits_per_sec"] = sb.get("bits_per_sec")
                merged["std_err_bits_per_sec"] = sb.get("std_err_bits_per_sec")
                merged["r_squared"] = sb.get("r_squared")
            out.append(merged)
        return out
    # Fall back to all_evaluations.json (no DSI / PD-rate available,
    # carry only what the driver wrote).
    for idx, row in enumerate(evaluation_rows):
        merged = dict(row)
        merged.setdefault("cell_index", idx)
        merged.setdefault("dsi_vector_sum", None)
        merged.setdefault("pd_rate_hz", None)
        merged.setdefault("silence_failed", False)
        merged["legit_bool"] = False
        out.append(merged)
    return out


def _write_predictions_jsonl_gz(*, cells: list[dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out_path, "wt", encoding="utf-8") as gz:
        for c in cells:
            gz.write(json.dumps(c) + "\n")


def _build_description_md(
    *,
    seed: int,
    n_cells: int,
    n_pareto: int,
    n_legit: int,
    best_mi_count_bits: float,
    min_atp_per_spike: float | None,
    hv_trajectory: list[dict[str, Any]],
    strong_bialek_summary: dict[str, Any],
    date_documented: str,
) -> str:
    final_gen = hv_trajectory[-1]["generation"] if len(hv_trajectory) > 0 else 0
    final_hv = hv_trajectory[-1]["hypervolume"] if len(hv_trajectory) > 0 else 0.0
    final_cost = hv_trajectory[-1]["cumulative_cost_usd"] if len(hv_trajectory) > 0 else 0.0
    min_atp_str = f"{min_atp_per_spike:.3e}" if min_atp_per_spike is not None else "n/a"
    sb_count = strong_bialek_summary.get("n_top10", 0)
    sb_max = strong_bialek_summary.get("max_bits_per_sec")
    sb_max_str = f"{sb_max:.1f}" if isinstance(sb_max, int | float) else "n/a"
    return (
        f"---\n"
        f'spec_version: "2"\n'
        f'predictions_id: "{PREDICTIONS_ID}"\n'
        f'documented_by_task: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"\n'
        f'date_documented: "{date_documented}"\n'
        f"---\n\n"
        f"# NSGA-II Predictions: MI vs ATP-per-Spike on Bed B + 14-d Morph\n\n"
        f"## Metadata\n\n"
        f"* **Name**: NSGA-II Pareto front: spike-count MI vs ATP-per-spike on "
        f"Bed B + 14-d morph\n"
        f"* **Model**: Procedural Bed B DSGC cell (t0090 generator + t0092 "
        f"z-axis soma patch, t0080 NEURON MOD channels)\n"
        f"* **Datasets**: (none; in-silico evaluation only)\n"
        f"* **Format**: jsonl.gz\n"
        f"* **Instances**: {n_cells}\n"
        f"* **Created by**: t0126_bedb_dsi_atp_per_spike_nsga2_60gen\n"
        f"* **GA seed**: {seed}\n"
        f"* **Generations completed**: {final_gen} / 60\n"
        f"* **Final cost (USD)**: ${final_cost:.4f} / $6.00 cap\n\n"
        f"## Overview\n\n"
        f"This predictions asset captures every per-cell evaluation from the "
        f"t0123 single-seed 68-d NSGA-II run on the Bed B + 14-d morphology "
        f"substrate. The 2-objective optimisation maximises spike-count MI "
        f"(Miller-Madow corrected, 4-direction antipodal protocol) and "
        f"simultaneously minimises ATP per spike (Sengupta 2010 recipe, "
        f"integrated inward Na charge across soma + AIS + every dendrite "
        f"compartment). DSI and PD-rate are tracked as diagnostics, not "
        f"optimised. The top-10 Pareto cells are additionally re-evaluated "
        f"post-hoc under the Strong-Bialek 1998 direct method at 8 directions "
        f"x 20 trials per direction to recover a literature-comparable bits/s "
        f"rate for the Niven 2007 comparison.\n\n"
        f"The run forks the t0122 NSGA-II substrate end-to-end (pop=96, "
        f"N_EVAL_SEEDS=3, _POOL_RESTART_EVERY=10, HV_PLATEAU_AUTO_STOP=False, "
        f"silence guard pd_spikes_sum < 3); the only behavioural deltas are "
        f"both objectives swapped to (MI, ATP/spike), N_DIRECTIONS raised "
        f"from 2 to 4, and the reduced `N_GEN_MAX = 60` / `COST_CAP_USD = 6.0` "
        f"constraints from the task description.\n\n"
        f"## Model\n\n"
        f"The cell is a procedural DSGC built by `generate_fixed_morphology` "
        f"(t0092 fix wrapper around t0090's generator) and parameterised by "
        f"the 14-d morphology vector concatenated with the 54-d electrophys "
        f"vector. The electrophys block uses the t0080 BedB v3 13-channel MOD "
        f"library (Nav1.6 + napt80 + nart80 sodium; KDR / Kv3 / Kv4 / Kv7 "
        f"potassium; BKT80 and SKAHPT80 calcium-activated potassium; IhT80; "
        f"T- and L-type calcium; SKT80). Synaptic inputs are AR(2)-correlated "
        f"ACh / GABA bundles placed by the parametric placer (t0024 de "
        f"Rosenroll 2026 ports), with NMDA conductance on dendrites. The AIS "
        f"is split into proximal / distal segments at the t0080-default ratio. "
        f"All parameters (channel densities, synapse weights, NMDA "
        f"conductance, AIS lengths, morphology branching parameters) are part "
        f"of the 68-d optimisation vector and vary per cell.\n\n"
        f"## Data\n\n"
        f"No external dataset is used. The evaluation is in-silico under a "
        f"4-direction antipodal-pair protocol: 4 angles (0, 90, 180, 270 deg) "
        f"x 3 evaluation seeds = 12 trials per cell, each 1400 ms of "
        f"simulated NEURON time at h.dt = 0.025 ms (TSTOP_MS = 1400). "
        f"Per-trial inputs are AR(2)-correlated Poisson event sequences over "
        f"the placed ACh and GABA synapses, with bar-arrival kinematic delays "
        f"derived from each synapse's xy coordinate on the realised "
        f"morphology. Inward Na current `seg.ina` is recorded at simulation "
        f"dt on every segment of the soma + AIS proximal + AIS distal + "
        f"every dendrite; AP windows are detected via somatic Vm threshold "
        f"crossings at -20 mV with a 2 ms refractory and integrated over "
        f"+/-2 ms around each peak.\n\n"
        f"## Prediction Format\n\n"
        f"The predictions file is `files/predictions.jsonl.gz` -- one row per "
        f"unique cell evaluated during the NSGA-II run, gzipped JSONL. "
        f"Per-row fields:\n\n"
        f"* `generation` -- generation index (0..60) when the cell was "
        f"evaluated\n"
        f"* `cell_index` -- 0-indexed identifier within the run\n"
        f"* `vector_68d` -- 54-d electrophys + 14-d morphology parameter "
        f"vector (concatenated)\n"
        f"* `mi_count_bits` -- spike-count MI in bits, Miller-Madow corrected, "
        f"4-direction contingency table\n"
        f"* `atp_per_spike_molecules` -- mean ATP molecules per AP across all "
        f"trials\n"
        f"* `atp_per_ap_molecules` -- same as `atp_per_spike_molecules` "
        f"(retained for back-compat)\n"
        f"* `atp_per_ap_compartment_breakdown` -- "
        f'{{"soma": float, "ais": float, "dendrites_total": float}}\n'
        f"* `firing_hz_per_dir` -- per-direction firing rate in Hz "
        f"(dir_0, dir_90, dir_180, dir_270)\n"
        f"* `dsi_vector_sum` -- vector-sum DSI in [0, 1] (tracked diagnostic)\n"
        f"* `pd_rate_hz` -- mean PD spike rate in Hz (tracked diagnostic)\n"
        f"* `objective_F_minimised` -- 2-tuple `[-mi_count_bits, "
        f"+atp_per_spike_molecules]` (F vector that NSGA-II minimised)\n"
        f"* `silence_failed_bool` (alias `silence_failed`) -- True iff "
        f"pd_spikes_sum < 3 OR ATP/spike was NaN\n"
        f"* `legit_bool` -- True iff DSI >= 0.5 AND PD-rate >= 30 Hz AND NOT "
        f"silence-failed\n\n"
        f"The {sb_count} cells included in the post-hoc Strong-Bialek rerun "
        f"additionally carry `mi_strong_bialek_bits_per_sec`, "
        f"`std_err_bits_per_sec`, and `r_squared`.\n\n"
        f"## Metrics\n\n"
        f"| Metric | Value |\n"
        f"|---|---|\n"
        f"| `n_cells_total` | {n_cells} |\n"
        f"| `n_legit_cells` (DSI >= 0.5, PD >= 30 Hz, NOT silence-failed) "
        f"| {n_legit} |\n"
        f"| `best_mi_count_bits` | {best_mi_count_bits:.4f} bits |\n"
        f"| `min_atp_per_spike_molecules` | {min_atp_str} |\n"
        f"| `n_pareto_cells` (driver final population) | {n_pareto} |\n"
        f"| `final_hypervolume` | {final_hv:.4f} |\n"
        f"| `final_cost_usd` | ${final_cost:.4f} |\n"
        f"| `top10_max_bits_per_sec` (Strong-Bialek) | {sb_max_str} |\n\n"
        f"## Main Ideas\n\n"
        f"* The 2-objective (max MI, min ATP/spike) Pareto front traces the "
        f"information-energy trade-off for the DSGC substrate at the resolution "
        f"of a 4-direction spike-count code (2-bit MI ceiling). The top-10 "
        f"cells re-evaluated under Strong-Bialek 1998 give the bits/s rate that "
        f"is directly comparable to the Niven 2007 fly-photoreceptor curve.\n"
        f"* DSI / PD-rate are computed and stored per cell for downstream "
        f"joint-pass filtering even though they do not enter the F vector; "
        f"the silence guard (`pd_spikes_sum < 3`) inherited from t0122 catches "
        f"cells that achieve low ATP/spike by simply not spiking and excludes "
        f"them from the LEGIT cohort.\n"
        f"* The Carter-Bean 2009 ATP/AP/cm benchmark at the AIS calibrates the "
        f"Sengupta 2010 recipe before launch; see the smoke gate report and "
        f"`results/images/carter_bean_atp_per_ap_check.png`.\n\n"
        f"## Summary\n\n"
        f"This predictions asset is the per-cell record of a single-seed "
        f"60-generation NSGA-II run optimising MI vs ATP-per-spike on the "
        f"68-d Bed B + 14-d morphology substrate. The run produced "
        f"{n_cells} unique cell evaluations at a final hypervolume of "
        f"{final_hv:.2f} and a total cost of ${final_cost:.4f}, within the "
        f"$6.00 cap. The asset includes the full per-cell 68-d vector plus "
        f"all evaluated diagnostics (MI, ATP/spike, per-compartment ATP "
        f"breakdown, per-direction firing rates, DSI / PD-rate, F vector, "
        f"silence-failure and LEGIT booleans). The top-{sb_count} Pareto "
        f"cells additionally carry Strong-Bialek 1998 direct-method MI in "
        f"bits/s for the Niven 2007 comparison documented in the companion "
        f"answer asset `dsgc-bits-per-atp-vs-niven-2007`.\n"
    )


def _build_details_json(
    *,
    seed: int,
    n_cells: int,
    n_pareto: int,
    n_legit: int,
    best_mi_count_bits: float,
    min_atp_per_spike: float | None,
    hv_trajectory: list[dict[str, Any]],
    strong_bialek_summary: dict[str, Any],
) -> dict[str, Any]:
    final_gen = hv_trajectory[-1]["generation"] if len(hv_trajectory) > 0 else 0
    final_hv = hv_trajectory[-1]["hypervolume"] if len(hv_trajectory) > 0 else 0.0
    final_cost = hv_trajectory[-1]["cumulative_cost_usd"] if len(hv_trajectory) > 0 else 0.0
    today = datetime.now(UTC).date().isoformat()
    return {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": "NSGA-II Pareto front: MI vs ATP-per-spike on Bed B + 14-d morph",
        "short_description": (
            "Per-cell evaluations from the t0123 68-d NSGA-II run optimising "
            "(maximise MI_count_bits, minimise ATP_per_spike) on the Bed B + "
            "14-d morphology substrate. 4-direction protocol, single GA seed, "
            "pop=96, N_EVAL_SEEDS=3, N_GEN_MAX=60, HV-plateau auto-stop "
            "disabled."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "Procedural Bed B DSGC cell with 14-d morphology parameter space "
            "(t0090 generator + t0092 z-axis soma patch) and 54-d electrophys "
            "parameter scheme (t0080 NEURON MOD channels). Evaluated under a "
            "4-direction antipodal protocol with AR(2)-correlated synaptic "
            "noise (t0024 de Rosenroll 2026 ports). ATP estimated from "
            "per-segment seg.ina inward integration per Sengupta 2010."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl.gz",
        "prediction_schema": (
            "Each row: {generation, cell_index, vector_68d, mi_count_bits, "
            "atp_per_spike_molecules, atp_per_ap_molecules, "
            "atp_per_ap_compartment_breakdown, firing_hz_per_dir, "
            "dsi_vector_sum, pd_rate_hz, objective_F_minimised, "
            "silence_failed_bool, legit_bool}. Top-N cells additionally carry "
            "{mi_strong_bialek_bits_per_sec, std_err_bits_per_sec, "
            "r_squared}. See description.md for full field definitions."
        ),
        "instance_count": int(n_cells),
        "metrics_at_creation": {
            "task_seed": int(seed),
            "n_generations_completed": int(final_gen),
            "n_cells_total": int(n_cells),
            "n_pareto_cells": int(n_pareto),
            "n_legit_cells": int(n_legit),
            "best_mi_count_bits": float(best_mi_count_bits),
            "min_atp_per_spike_molecules": (
                float(min_atp_per_spike) if min_atp_per_spike is not None else None
            ),
            "final_hypervolume": float(final_hv),
            "final_cost_usd": float(final_cost),
            "top10_max_bits_per_sec": strong_bialek_summary.get("max_bits_per_sec"),
            "top10_min_bits_per_sec": strong_bialek_summary.get("min_bits_per_sec"),
            "top10_mean_bits_per_sec": strong_bialek_summary.get("mean_bits_per_sec"),
            "niven_2007_above_below_count": strong_bialek_summary.get(
                "niven_above_below_count",
            ),
        },
        "files": [
            {
                "path": "files/predictions.jsonl.gz",
                "description": (
                    "Gzipped JSONL with one row per unique cell evaluated by "
                    "the NSGA-II run. See description.md and prediction_schema."
                ),
                "format": "jsonl.gz",
            }
        ],
        "categories": [
            "direction-selectivity",
            "compartmental-modeling",
            "dendritic-computation",
            "retinal-ganglion-cell",
        ],
        "created_by_task": "t0126_bedb_dsi_atp_per_spike_nsga2_60gen",
        "date_created": today,
    }


def _summarise_strong_bialek(*, sb_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if len(sb_map) == 0:
        return {
            "n_top10": 0,
            "max_bits_per_sec": None,
            "min_bits_per_sec": None,
            "mean_bits_per_sec": None,
            "niven_above_below_count": None,
        }
    values: list[float] = []
    for entry in sb_map.values():
        v = entry.get("bits_per_sec")
        if isinstance(v, int | float) and (v == v):  # not NaN
            values.append(float(v))
    if len(values) == 0:
        return {
            "n_top10": len(sb_map),
            "max_bits_per_sec": None,
            "min_bits_per_sec": None,
            "mean_bits_per_sec": None,
            "niven_above_below_count": None,
        }
    return {
        "n_top10": len(sb_map),
        "max_bits_per_sec": float(max(values)),
        "min_bits_per_sec": float(min(values)),
        "mean_bits_per_sec": float(sum(values) / len(values)),
        "niven_above_below_count": None,
    }


def build_predictions_asset(*, seed: int) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    eval_rows = _load_all_evaluations(seed=seed)
    trace_rows = _load_cell_trace_jsonl(seed=seed)
    pareto_cells = _load_pareto(seed=seed)
    hv_trajectory = _load_hv_trajectory(seed=seed)
    sb_map = _load_strong_bialek_top10()
    sb_summary = _summarise_strong_bialek(sb_map=sb_map)

    cells = _merge_rows(
        trace_rows=trace_rows,
        evaluation_rows=eval_rows,
        strong_bialek_map=sb_map,
    )
    n_cells = len(cells)
    n_pareto = len(pareto_cells)
    legit_cells = [c for c in cells if bool(c.get("legit_bool", False))]
    n_legit = len(legit_cells)
    best_mi = max(
        (
            float(c["mi_count_bits"])
            for c in cells
            if isinstance(c.get("mi_count_bits"), int | float)
        ),
        default=0.0,
    )
    finite_atp = [
        float(c["atp_per_spike_molecules"])
        for c in cells
        if isinstance(c.get("atp_per_spike_molecules"), int | float)
        and c["atp_per_spike_molecules"] > 0.0
        and c["atp_per_spike_molecules"] < 1e15
    ]
    min_atp = min(finite_atp) if len(finite_atp) > 0 else None

    _write_predictions_jsonl_gz(cells=cells, out_path=PREDICTIONS_JSONL_GZ)
    print(
        f"[predictions] wrote {PREDICTIONS_JSONL_GZ} "
        f"({PREDICTIONS_JSONL_GZ.stat().st_size / 1024:.1f} KB) "
        f"with {n_cells} cells"
    )

    details = _build_details_json(
        seed=seed,
        n_cells=n_cells,
        n_pareto=n_pareto,
        n_legit=n_legit,
        best_mi_count_bits=best_mi,
        min_atp_per_spike=min_atp,
        hv_trajectory=hv_trajectory,
        strong_bialek_summary=sb_summary,
    )
    DETAILS_PATH.write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"[predictions] wrote {DETAILS_PATH}")

    date_documented = datetime.now(UTC).date().isoformat()
    description = _build_description_md(
        seed=seed,
        n_cells=n_cells,
        n_pareto=n_pareto,
        n_legit=n_legit,
        best_mi_count_bits=best_mi,
        min_atp_per_spike=min_atp,
        hv_trajectory=hv_trajectory,
        strong_bialek_summary=sb_summary,
        date_documented=date_documented,
    )
    DESCRIPTION_PATH.write_text(description, encoding="utf-8")
    print(f"[predictions] wrote {DESCRIPTION_PATH}")

    return ASSET_DIR


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed",
        type=int,
        default=int(T0129_SEEDS[0]),
    )
    args = parser.parse_args()
    build_predictions_asset(seed=int(args.seed))


if __name__ == "__main__":
    main()
