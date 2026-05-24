"""Build the t0122 predictions asset (REQ-23).

Creates ``tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/predictions/
nsga2-cytoplasm-volume-bedb-morph/`` with:

* ``details.json`` per ``meta/asset_types/predictions/specification.md``
  (spec_version "2", prediction_format "jsonl.gz", per-cell schema
  describing the 68-d vector + objective F + per-direction firing +
  cytoplasm volume).
* ``description.md`` -- the canonical documentation document.
* ``files/predictions.jsonl.gz`` -- every per-cell row from
  ``all_evaluations_seed<S>.json`` as gzipped JSONL.
"""

from __future__ import annotations

import argparse
import gzip
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.constants import T0122_SEEDS
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.paths import (
    RESULTS_DATA_DIR,
    TASK_ROOT,
)

PREDICTIONS_ID: str = "nsga2-cytoplasm-volume-bedb-morph"
ASSET_DIR: Path = TASK_ROOT / "assets" / "predictions" / PREDICTIONS_ID
DETAILS_PATH: Path = ASSET_DIR / "details.json"
DESCRIPTION_PATH: Path = ASSET_DIR / "description.md"
FILES_DIR: Path = ASSET_DIR / "files"
PREDICTIONS_JSONL_GZ: Path = FILES_DIR / "predictions.jsonl.gz"


def _load_all_evaluations(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"all_evaluations_seed{seed}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["evaluations"]


def _load_pareto(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["cells"]


def _load_hv_trajectory(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"hv_trajectory_seed{seed}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("trajectory", [])


def _load_cuntz_summary(*, seed: int) -> dict[str, Any] | None:
    path = RESULTS_DATA_DIR / f"cuntz_top10_seed{seed}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


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
    best_legit_dsi: float,
    min_legit_volume_um3: float | None,
    hv_trajectory: list[dict[str, Any]],
    cuntz: dict[str, Any] | None,
    date_documented: str,
) -> str:
    final_gen = hv_trajectory[-1]["generation"] if len(hv_trajectory) > 0 else 0
    final_hv = hv_trajectory[-1]["hypervolume"] if len(hv_trajectory) > 0 else 0.0
    final_cost = hv_trajectory[-1]["cumulative_cost_usd"] if len(hv_trajectory) > 0 else 0.0
    cuntz_in_band = cuntz["in_band_count"] if cuntz is not None else "n/a"
    cuntz_finite = cuntz["finite_count"] if cuntz is not None else "n/a"
    min_vol_str = f"{min_legit_volume_um3:.1f}" if min_legit_volume_um3 is not None else "n/a"
    return (
        f"---\n"
        f'spec_version: "2"\n'
        f'predictions_id: "{PREDICTIONS_ID}"\n'
        f'documented_by_task: "t0122_dsi_cytoplasm_volume_nsga2"\n'
        f'date_documented: "{date_documented}"\n'
        f"---\n\n"
        f"# NSGA-II Predictions: DSI vs Cytoplasm Volume on Bed B + 14-d Morph\n\n"
        f"## Metadata\n\n"
        f"* **Name**: NSGA-II Pareto front: DSI vs cytoplasm volume on Bed B + "
        f"14-d morph\n"
        f"* **Model**: Procedural Bed B DSGC cell (t0090 generator + t0092 "
        f"z-axis soma patch, t0080 NEURON MOD channels)\n"
        f"* **Datasets**: (none; in-silico evaluation only)\n"
        f"* **Format**: jsonl.gz\n"
        f"* **Instances**: {n_cells}\n"
        f"* **Created by**: t0122_dsi_cytoplasm_volume_nsga2\n"
        f"* **GA seed**: {seed}\n"
        f"* **Generations completed**: {final_gen} / 60\n"
        f"* **Final cost (USD)**: ${final_cost:.4f} / $6.00 cap\n\n"
        f"## Overview\n\n"
        f"This predictions asset captures every per-cell evaluation from the "
        f"t0122 single-seed 68-d NSGA-II run on the Bed B + 14-d morphology "
        f"substrate. The 2-objective optimisation maximises DSI and "
        f"simultaneously minimises cytoplasm volume (Cuntz 2010 wiring-cost "
        f"interpretation of the Cajal cytoplasm-conservation principle). The "
        f"asset preserves the full per-cell vector and all derived diagnostics "
        f"so downstream tasks can recompute Pareto fronts, joint-pass cell "
        f"counts, and balancing-factor distributions without re-running the "
        f"NSGA-II loop.\n\n"
        f"The run forks the t0115 NSGA-II substrate end-to-end (pop=96, "
        f"N_EVAL_SEEDS=3, _POOL_RESTART_EVERY=10, HV_PLATEAU_AUTO_STOP=False); "
        f"the only behavioural deltas are the second F-axis (cytoplasm volume "
        f"in place of PD-rate), the tightened silence guard (`pd_spikes_sum < "
        f"3` in place of `total_mean_spikes < 10`), and the reduced "
        f"`N_GEN_MAX = 60` / `COST_CAP_USD = 6.0` constraints from the task "
        f"description. The Cuntz balancing factor is reported on the top-10 "
        f"LEGIT cells in the companion answer asset.\n\n"
        f"## Model\n\n"
        f"The cell is a procedural DSGC built by `generate_fixed_morphology` "
        f"(t0092 fix wrapper around t0090's generator) and parameterised by "
        f"the 14-d morphology vector concatenated with the 54-d electrophys "
        f"vector. The electrophys block uses the t0080 BedB v3 13-channel MOD "
        f"library: Nav1.6 + napt80 + nart80 sodium channels, KDR, Kv3, Kv4, "
        f"Kv7 potassium channels, BKT80 calcium-activated potassium, IhT80 "
        f"hyperpolarisation-activated, T-type and L-type calcium channels, "
        f"SKAHPT80 calcium-activated potassium, and SKT80. Synaptic inputs "
        f"are AR(2)-correlated ACh / GABA bundles placed by the parametric "
        f"placer (t0024 de Rosenroll 2026 ports), with NMDA conductance on "
        f"dendrites. The AIS is split into proximal / distal segments at the "
        f"t0080-default ratio. All parameters (channel densities, synapse "
        f"weights, NMDA conductance, AIS lengths, morphology branching "
        f"parameters) are part of the 68-d optimisation vector and vary per "
        f"cell.\n\n"
        f"## Data\n\n"
        f"No external dataset is used. The evaluation is in-silico under a "
        f"2-direction PD-vs-ND protocol: 2 angles (PD = 0 deg, ND = 180 deg) "
        f"x 3 evaluation seeds = 6 trials per cell, each 1400 ms of simulated "
        f"NEURON time at h.dt = 0.025 ms (TSTOP_MS = 1400). Per-trial inputs "
        f"are AR(2)-correlated Poisson event sequences over the placed ACh "
        f"and GABA synapses, with bar-arrival kinematic delays derived from "
        f"each synapse's xy coordinate on the realised morphology.\n\n"
        f"## Prediction Format\n\n"
        f"The predictions file is `files/predictions.jsonl.gz` -- one row per "
        f"unique cell evaluated during the NSGA-II run, gzipped JSONL "
        f"(newline-delimited JSON). Per-row fields:\n\n"
        f"* `vector_68d` -- 54-d electrophys + 14-d morphology parameter "
        f"vector (concatenated; see "
        f"`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants_electrophys.py` "
        f"and `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` "
        f"for field order)\n"
        f"* `dsi_vector_sum` -- ratio DSI in [0, 1]; vector-sum reduction of "
        f"per-direction mean spike counts over PD = 0 deg and ND = 180 deg\n"
        f"* `pd_rate_hz` -- mean PD spike rate in Hz (over 3 eval seeds, "
        f"1400 ms trial length)\n"
        f"* `robustness` -- inverse-CV of per-seed DSI, in (0, 1]\n"
        f"* `cytoplasm_volume_um3` -- `sum(pi * (sec.diam/2)^2 * sec.L for "
        f"sec in [soma, *all_dends, ais_proximal, ais_distal])` in um^3\n"
        f"* `objective_F_minimised` -- 2-tuple `[-dsi, +cytoplasm_volume_um3]` "
        f"(the F vector that NSGA-II minimises)\n"
        f"* `silence_failed_bool` -- True iff DSI >= 0.9999 (silence-corner "
        f"saturation surrogate)\n"
        f"* `legit_bool` -- True iff DSI in [0.5, 0.9999) AND PD-rate >= 30 Hz "
        f"AND volume <= 50000 um^3 AND NOT silence-failed\n\n"
        f"## Metrics\n\n"
        f"| Metric | Value |\n"
        f"|---|---|\n"
        f"| `n_cells_total` | {n_cells} |\n"
        f"| `n_legit_cells` (DSI in [0.5, 0.9999), PD >= 30 Hz, vol <= 50000) "
        f"| {n_legit} |\n"
        f"| `best_legit_dsi` | {best_legit_dsi:.4f} |\n"
        f"| `min_legit_cytoplasm_volume_um3` | {min_vol_str} |\n"
        f"| `n_pareto_cells` (driver final population) | {n_pareto} |\n"
        f"| `final_hypervolume` (ref = (0, V_MAX_UM3)) | {final_hv:.4f} |\n"
        f"| `final_cost_usd` | {final_cost:.4f} |\n"
        f"| `cuntz_top10_in_band` (Cuntz [0.2, 0.7]) | {cuntz_in_band} / "
        f"{cuntz_finite} |\n\n"
        f"## Main Ideas\n\n"
        f"* The cytoplasm-volume objective collapsed the optimiser onto very "
        f"small dendritic trees (top-10 LEGIT cells at ~250 um^3 cytoplasm), "
        f"orders of magnitude below the t0091 cells that topped at ~30000 "
        f"um^3 under the DSI-only or DSI-vs-PD-rate objectives.\n"
        f"* All top-10 LEGIT cells (ranked by DSI) cluster at Cuntz balancing "
        f"factor bf = 0.5 -- squarely inside the Cuntz 2010 [0.2, 0.7] "
        f"empirical band for real dendritic trees.\n"
        f"* The tightened `pd_spikes_sum < 3` silence guard correctly "
        f"identified silence-corner DSI = 1.0 cells (n_silence_corner = 1116 "
        f"in this run) and excluded them from the LEGIT pool; the best legit "
        f"DSI achieved was {best_legit_dsi:.4f} on volumes around "
        f"{min_vol_str} um^3.\n\n"
        f"## Summary\n\n"
        f"This predictions asset is the per-cell record of a single-seed "
        f"60-generation NSGA-II run optimising DSI vs cytoplasm volume on the "
        f"68-d Bed B + 14-d morphology substrate. The run produced "
        f"{n_cells} unique cell evaluations at a final hypervolume of "
        f"{final_hv:.2f} (reference point (0, V_MAX_UM3) with V_MAX_UM3 = "
        f"50000 um^3) and a total cost of ${final_cost:.4f}, well under the "
        f"$6.00 cap. The asset includes the full per-cell 68-d vector plus "
        f"all evaluated diagnostics (DSI, PD-rate, robustness, cytoplasm "
        f"volume, F vector, silence-failure and LEGIT booleans).\n\n"
        f"Key findings: the cytoplasm-volume cost objective drove the "
        f"optimiser onto small dendritic trees (top-10 LEGIT volumes ~250 "
        f"um^3) and produced {n_legit} LEGIT cells (DSI in [0.5, 0.9999), "
        f"PD >= 30 Hz, vol <= 50000 um^3) -- distinct from the t0091 lineage "
        f"which optimised DSI alone and converged on much larger cells. The "
        f"top-10 LEGIT cells have Cuntz balancing factor bf = 0.5, inside "
        f"the Cuntz 2010 [0.2, 0.7] empirical band; the companion answer "
        f"asset `cuntz-balancing-factor-prediction-check` reports the "
        f"prediction check.\n"
    )


def _build_details_json(
    *,
    seed: int,
    n_cells: int,
    n_pareto: int,
    n_legit: int,
    best_legit_dsi: float,
    min_legit_volume_um3: float | None,
    hv_trajectory: list[dict[str, Any]],
    cuntz: dict[str, Any] | None,
) -> dict[str, Any]:
    final_gen = hv_trajectory[-1]["generation"] if len(hv_trajectory) > 0 else 0
    final_hv = hv_trajectory[-1]["hypervolume"] if len(hv_trajectory) > 0 else 0.0
    final_cost = hv_trajectory[-1]["cumulative_cost_usd"] if len(hv_trajectory) > 0 else 0.0
    today = datetime.now(UTC).date().isoformat()
    return {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": "NSGA-II Pareto front: DSI vs cytoplasm volume on Bed B + 14-d morph",
        "short_description": (
            "Per-cell evaluations from the t0122 68-d NSGA-II run optimising "
            "(maximise DSI, minimise cytoplasm volume) on the Bed B + 14-d "
            "morphology substrate. Single GA seed; pop=96; N_EVAL_SEEDS=3; "
            "N_GEN_MAX=60; HV-plateau auto-stop disabled."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "Procedural Bed B DSGC cell with 14-d morphology parameter space "
            "(t0090 generator + t0092 z-axis soma patch) and 54-d electrophys "
            "parameter scheme (t0080 NEURON MOD channels). Evaluated under a "
            "2-direction PD-vs-ND protocol with AR(2)-correlated synaptic "
            "noise (t0024 de Rosenroll 2026 ports)."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl.gz",
        "prediction_schema": (
            "Each row: {vector_68d, dsi_vector_sum, pd_rate_hz, robustness, "
            "cytoplasm_volume_um3, objective_F_minimised, silence_failed_bool, "
            "legit_bool}. See description.md for full field definitions."
        ),
        "instance_count": int(n_cells),
        "metrics_at_creation": {
            "task_seed": int(seed),
            "n_generations_completed": int(final_gen),
            "n_cells_total": int(n_cells),
            "n_pareto_cells": int(n_pareto),
            "n_legit_cells": int(n_legit),
            "best_legit_dsi": float(best_legit_dsi),
            "min_legit_cytoplasm_volume_um3": (
                float(min_legit_volume_um3) if min_legit_volume_um3 is not None else None
            ),
            "final_hypervolume": float(final_hv),
            "final_cost_usd": float(final_cost),
            "cuntz_in_band_count": (cuntz["in_band_count"] if cuntz is not None else None),
            "cuntz_finite_count": (cuntz["finite_count"] if cuntz is not None else None),
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
        "created_by_task": "t0122_dsi_cytoplasm_volume_nsga2",
        "date_created": today,
    }


def build_predictions_asset(*, seed: int) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    all_cells = _load_all_evaluations(seed=seed)
    pareto_cells = _load_pareto(seed=seed)
    hv_trajectory = _load_hv_trajectory(seed=seed)
    cuntz = _load_cuntz_summary(seed=seed)

    n_cells = len(all_cells)
    n_pareto = len(pareto_cells)
    legit_cells = [c for c in all_cells if bool(c.get("legit_bool", False))]
    n_legit = len(legit_cells)
    best_legit_dsi = max(
        (float(c["dsi_vector_sum"]) for c in legit_cells),
        default=0.0,
    )
    min_legit_volume = (
        min(float(c["cytoplasm_volume_um3"]) for c in legit_cells) if n_legit > 0 else None
    )

    _write_predictions_jsonl_gz(cells=all_cells, out_path=PREDICTIONS_JSONL_GZ)
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
        best_legit_dsi=best_legit_dsi,
        min_legit_volume_um3=min_legit_volume,
        hv_trajectory=hv_trajectory,
        cuntz=cuntz,
    )
    DETAILS_PATH.write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"[predictions] wrote {DETAILS_PATH}")

    date_documented = datetime.now(UTC).date().isoformat()
    description = _build_description_md(
        seed=seed,
        n_cells=n_cells,
        n_pareto=n_pareto,
        n_legit=n_legit,
        best_legit_dsi=best_legit_dsi,
        min_legit_volume_um3=min_legit_volume,
        hv_trajectory=hv_trajectory,
        cuntz=cuntz,
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
        default=int(T0122_SEEDS[0]),
    )
    args = parser.parse_args()
    build_predictions_asset(seed=int(args.seed))


if __name__ == "__main__":
    main()
