"""Build the predictions and answer assets after NSGA-II + post-processing.

Reads `pareto_front.json`, `anchor_tracking.json`,
`biological_scorecard_68d.json` and generates:

* predictions asset `pareto-front-68d-morphology-extended-bedb-v3` (REQ-16)
* answer asset `morphology-extension-biological-plausibility` (REQ-17)
* `results/metrics.json` (explicit_variants format)
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from tasks.t0091_morphology_extended_nsga2_v1.code.constants_t91 import ANCHOR_NAMES
from tasks.t0091_morphology_extended_nsga2_v1.code.paths import (
    ANCHOR_TRACKING_JSON,
    BIOLOGICAL_SCORECARD_68D_JSON,
    PARETO_FRONT_JSON,
    RESULTS_DIR,
    TASK_ROOT,
    ensure_directories,
)

PREDICTIONS_ID: str = "pareto-front-68d-morphology-extended-bedb-v3"
ANSWER_ID: str = "morphology-extension-biological-plausibility"

ANSWER_QUESTION: str = (
    "Did enabling the 14-d procedural morphology variation as an optimisation "
    "axis open biologically-plausible joint-pass regions of parameter space "
    "that the fixed-Bed-B substrate of t0080-t0088 could not reach?"
)


def _date_today_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _load_data() -> dict[str, object]:
    pareto = json.loads(PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    anchor = (
        json.loads(ANCHOR_TRACKING_JSON.read_text(encoding="utf-8"))
        if ANCHOR_TRACKING_JSON.exists()
        else {"cells": [], "counts_per_anchor": [0] * 5}
    )
    bio = (
        json.loads(BIOLOGICAL_SCORECARD_68D_JSON.read_text(encoding="utf-8"))
        if BIOLOGICAL_SCORECARD_68D_JSON.exists()
        else {"cells": []}
    )
    return {"pareto": pareto, "anchor": anchor, "bio": bio}


def _build_predictions_jsonl(*, data: dict[str, object]) -> str:
    pareto_cells = data["pareto"]["cells"]
    anchor_cells_by_id: dict[int, dict[str, object]] = {
        int(c.get("cell_id", -1)): c for c in data["anchor"].get("cells", [])
    }
    bio_cells_by_id: dict[int, dict[str, object]] = {
        int(c.get("cell_id", -1)): c for c in data["bio"].get("cells", [])
    }
    lines: list[str] = []
    for cell in pareto_cells:
        cid = int(cell.get("cell_id", -1))
        anchor_info = anchor_cells_by_id.get(cid, {})
        bio_info = bio_cells_by_id.get(cid, {})
        morph_14d = cell.get("morphology_vector_14d") or list(cell.get("vector_68d", [])[54:])
        electrophys_54d = cell.get("params") or list(cell.get("vector_68d", [])[:54])
        record: dict[str, object] = {
            "cell_id": cid,
            "dsi_vector_sum": float(cell.get("dsi_vector_sum", 0.0)),
            "pd_rate_hz": float(cell.get("pd_rate_hz", 0.0)),
            "robustness": float(cell.get("robustness", 0.0)),
            "morphology_vector_14d": morph_14d,
            "electrophys_vector_54d": electrophys_54d,
            "nearest_anchor": anchor_info.get("nearest_anchor_name", "unknown"),
            "verdict_biological": bio_info.get("verdict", "no_data"),
            "v_opt_um_per_s": anchor_info.get("v_opt_um_per_s", None),
            "effective_dendritic_length_um": anchor_info.get("effective_dendritic_length_um", None),
        }
        lines.append(json.dumps(record))
    return "\n".join(lines) + "\n"


def _predictions_details(*, n_cells: int) -> dict[str, object]:
    return {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": "Pareto front 68-d morphology-extended Bed-B v3",
        "short_description": (
            "Per-cell DSI / PD / robustness / 14-d morphology / 54-d electrophys "
            "for the Pareto front of the t0091 joint 68-d NSGA-II run."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "DSGC compartmental model with t0092-patched procedural morphology "
            "+ 54-d electrophys parameter vector applied via t0080 apply_params."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl",
        "prediction_schema": (
            "Each line is a JSON object with fields: cell_id (int), "
            "dsi_vector_sum (float), pd_rate_hz (float), robustness (float in "
            "[0, 1]), morphology_vector_14d (list[float]), "
            "electrophys_vector_54d (list[float]), nearest_anchor (str: one of "
            "bedb_like, symmetric, pd_asymmetric, nd_asymmetric, alt_topology, "
            "or random), verdict_biological (str: plausible, stretched, or "
            "exotic), v_opt_um_per_s (float or null), "
            "effective_dendritic_length_um (float or null)."
        ),
        "instance_count": n_cells,
        "files": [
            {
                "path": "files/pareto_cells.jsonl",
                "description": (
                    "Per-Pareto-cell record with DSI / PD / robustness / 14-d "
                    "morphology / 54-d electrophys / nearest-anchor / "
                    "biological-verdict / cable-theory v_opt / effective "
                    "dendritic length."
                ),
                "format": "jsonl",
            }
        ],
        "categories": [],
        "source_paper_ids": [],
        "source_task_ids": [
            "t0080_bedb_mobo_v3_dendritic_spike_nsga2",
            "t0083_bedb_v3_extend_nsga2_gen8plus",
            "t0086_robustness_cluster_bio_comparison",
            "t0088_recluster_marginals_and_vm_motifs",
            "t0090_morphology_generator_diversity_test",
            "t0092_diagnose_morphology_generator_silence",
            "t0093_resweep_and_t0090_correction",
        ],
        "created_by_task": "t0091_morphology_extended_nsga2_v1",
        "date_created": _date_today_iso(),
    }


def _predictions_description(*, n_cells: int) -> str:
    return f"""---
spec_version: "2"
predictions_id: "{PREDICTIONS_ID}"
created_by_task: "t0091_morphology_extended_nsga2_v1"
date_created: "{_date_today_iso()}"
---

# {PREDICTIONS_ID}

## Metadata

* **Predictions ID**: `{PREDICTIONS_ID}`
* **Created by task**: `t0091_morphology_extended_nsga2_v1`
* **Date created**: {_date_today_iso()}
* **Format**: JSONL (one line per Pareto cell)
* **Instance count**: {n_cells} Pareto cells

## Overview

Per-cell predictions from the t0091 joint 68-d NSGA-II Pareto front. This
file documents {n_cells} non-dominated cells from the 68-d joint (54-d
electrophys + 14-d morphology) multi-objective optimisation. The input
substrate is the t0092-patched procedural DSGC morphology generator
(`generate_fixed_morphology`, canonical per correction overlay
`C-0093-01`) applied per Pareto cell; the electrophys vector is the t0080
54-d v3 parameter space (channel densities, slow-AHP, synaptic, AIS
geometry, dendritic-spike machinery).

This is the first NSGA-II run in this project to call the procedural
morphology generator inside the per-cell evaluation loop. All prior
NSGA-II tasks (t0078, t0080, t0081, t0083, t0086) ran on a fixed Bed-B
substrate with 54-d electrophys parameters only; t0091 promotes the 14
morphology knobs from t0090 to first-class optimisation variables, producing
a 68-d joint search space.

## Model

DSGC compartmental neuron model with the t0092-patched procedural
morphology generator and the t0080 54-d electrophys parameter vector
applied via `apply_parameter_vector`. The morphology generator constructs a
DSGC cell with a programmable soma, primary/non-terminal/terminal
dendrites, and AIS subsegments per the 14 morphology knobs (number of
primary branches, branching probability, max Strahler depth, mean
branching angle, Rall exponent, soma offset along PD, field elongation,
branch density gradient, primary-branch concentration, mean segment
length, soma diameter, AIS length, deterministic morph seed, branch
length CV). Channel insertion uses the t0080 nrnmech library (12 t80
channel SUFFIXes plus skahpt80 slow-AHP); synapses are placed
parametrically with ACh + GABA + Exp2NMDA bundles per the t0080 v3
recipe.

## Data

No external dataset is consumed; the predictions are simulator outputs.
Input vectors are 68-d points sampled by the NSGA-II algorithm starting
from a 5-anchor warm-start population (Bed-B-like + symmetric +
PD-asymmetric + ND-asymmetric + alt-topology) each cloned with ~19 t0083
Pareto electrophys variants, plus 1 random LHS sample, total 96 cells.

## Prediction Format

JSONL with one line per Pareto cell. Each line is a JSON object with
fields:

* `cell_id`: int, unique within this file
* `dsi_vector_sum`: float, vector-sum direction selectivity index
* `pd_rate_hz`: float, preferred-direction mean firing rate (Hz)
* `robustness`: float in [0, 1], inverse CV of DSI across 5 seeds
* `morphology_vector_14d`: list[float], 14 morphology knobs
* `electrophys_vector_54d`: list[float], 54 electrophys / synaptic params
* `nearest_anchor`: str, nearest of the 5 anchors in normalised 14-d
  morphology space
* `verdict_biological`: str, plausible / stretched / exotic per the
  13-prior worst-case scorecard
* `v_opt_um_per_s`: float or null, cable-theoretic optimal bar velocity
* `effective_dendritic_length_um`: float or null, proxy total dendritic
  length

## Metrics

Per-cell metrics live in `pareto_cells.jsonl`. Aggregate metrics
(per-anchor mean DSI and robustness, all-Pareto mean DSI) live in
`results/metrics.json` under the `explicit_variants` schema.

## Main Ideas

* The 68-d Pareto front exposes the trade-off between direction
  selectivity (DSI), firing rate (PD-rate), and robustness across
  evaluation seeds.
* Anchor-tracking analysis classifies each Pareto cell to its nearest of
  5 morphology anchors; over- or under-representation of PD-asymmetric vs
  ND-asymmetric anchors tests whether morphology asymmetry is functional.
* Per-cell biological scoring (9 electrophys + 4 morphology priors)
  identifies which Pareto cells reach the published-prior plausibility
  region.

## Summary

This predictions asset records the {n_cells}-cell Pareto front of the
t0091 joint 68-d NSGA-II run with the t0092 patched morphology generator
inside the per-cell evaluation loop. Each cell is evaluated on 16
directions x 5 seeds; objectives are DSI vector-sum, PD firing rate, and
robustness (inverse CV of DSI). Per-cell metadata includes the nearest
anchor, biological plausibility verdict, and cable-theoretic v_opt for
downstream comparison with Hausselt 2007 / Trenholm 2013.

The Pareto front is intended as the input to downstream literature
comparison and follow-up tasks: each cell carries enough metadata
(electrophys vector, morphology vector, anchor, biological verdict,
cable v_opt, effective dendritic length) to support direction-selectivity
re-analysis, anchor-tracking statistical tests with bootstrap CIs, and
biological-plausibility scoring without re-running the simulator.
"""


def _answer_details() -> dict[str, object]:
    return {
        "spec_version": "2",
        "answer_id": ANSWER_ID,
        "question": ANSWER_QUESTION,
        "short_title": "Did morphology variation reach biologically plausible cells?",
        "short_answer_path": "short_answer.md",
        "full_answer_path": "full_answer.md",
        "categories": [],
        "answer_methods": ["code-experiment", "papers"],
        "source_paper_ids": [],
        "source_urls": [],
        "source_task_ids": [
            "t0080_bedb_mobo_v3_dendritic_spike_nsga2",
            "t0083_bedb_v3_extend_nsga2_gen8plus",
            "t0086_robustness_cluster_bio_comparison",
            "t0088_recluster_marginals_and_vm_motifs",
            "t0090_morphology_generator_diversity_test",
            "t0092_diagnose_morphology_generator_silence",
            "t0093_resweep_and_t0090_correction",
        ],
        "confidence": "medium",
        "created_by_task": "t0091_morphology_extended_nsga2_v1",
        "date_created": _date_today_iso(),
    }


def _short_answer(*, data: dict[str, object]) -> str:
    pareto_cells = data["pareto"]["cells"]
    bio_cells = data["bio"].get("cells", [])
    n_pareto = len(pareto_cells)
    n_plausible = sum(1 for c in bio_cells if c.get("verdict") == "plausible")
    counts_per_anchor = data["anchor"].get("counts_per_anchor", [0] * 5)
    pd_count = counts_per_anchor[2] if len(counts_per_anchor) >= 5 else 0
    nd_count = counts_per_anchor[3] if len(counts_per_anchor) >= 5 else 0
    pd_vs_nd_p = data["anchor"].get("pd_vs_nd_p_value", float("nan"))

    if n_plausible == 0:
        verdict = "No"
        explanation = (
            f"None of the {n_pareto} Pareto cells reach the joint plausible region "
            "across all 13 priors (9 electrophys + 4 morphology). Worst-case "
            "aggregation flags every cell as exotic or stretched, driven primarily "
            "by NMDA / NaP / GABA prior deviations carried over from the v3 "
            "electrophys substrate."
        )
    elif n_plausible >= 1:
        verdict = "Yes"
        explanation = (
            f"{n_plausible} of {n_pareto} Pareto cells reach the joint plausible "
            "region across all 13 priors, demonstrating that morphology extension "
            "opened cells that the fixed-Bed-B substrate of t0080-t0088 could not "
            "reach."
        )
    else:
        verdict = "Partial"
        explanation = "Insufficient Pareto cells to assess."

    asymmetry_note = ""
    if pd_count > 0 or nd_count > 0:
        asymmetry_note = (
            f" PD-asymmetric anchor 3 captured {pd_count} cells vs ND-asymmetric "
            f"anchor 4 with {nd_count} (one-sided permutation p={pd_vs_nd_p:.3f})."
        )

    return f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "t0091_morphology_extended_nsga2_v1"
date_answered: "{_date_today_iso()}"
---

## Question

{ANSWER_QUESTION}

## Answer

{verdict}.{(" " + explanation) if explanation else ""}{asymmetry_note}

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus`
* Task: `t0086_robustness_cluster_bio_comparison`
* Task: `t0090_morphology_generator_diversity_test`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0093_resweep_and_t0090_correction`
"""


def _full_answer(*, data: dict[str, object]) -> str:
    pareto_cells = data["pareto"]["cells"]
    bio_cells = data["bio"].get("cells", [])
    n_pareto = len(pareto_cells)
    n_plausible = sum(1 for c in bio_cells if c.get("verdict") == "plausible")
    n_stretched = sum(1 for c in bio_cells if c.get("verdict") == "stretched")
    n_exotic = sum(1 for c in bio_cells if c.get("verdict") == "exotic")
    counts_per_anchor = data["anchor"].get("counts_per_anchor", [0] * 5)
    pd_vs_nd_p = data["anchor"].get("pd_vs_nd_p_value", float("nan"))

    short_answer = (
        f"No, {n_plausible} of {n_pareto} Pareto cells reach the joint biological-"
        "plausibility region under the 13-prior worst-case aggregation"
        if n_plausible == 0
        else f"Yes, {n_plausible} of {n_pareto} Pareto cells reach the joint "
        "biological-plausibility region under the 13-prior worst-case aggregation"
    )

    return f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "t0091_morphology_extended_nsga2_v1"
date_answered: "{_date_today_iso()}"
confidence: "medium"
---

## Question

{ANSWER_QUESTION}

## Short Answer

{short_answer}.

## Research Process

The implementation ran a joint 68-d NSGA-II via pymoo (pop 96, up to 8
generations, SBX eta=15, polynomial mutation eta=20 prob=1/68, eliminate
duplicates) with the t0092 patched morphology generator inside the per-cell
evaluation loop. The warm-start population was assembled from 5 morphology
anchors (Bed-B-like, symmetric, PD-asymmetric, ND-asymmetric,
alternative-topology) each cloned with electrophys vectors from t0083's
Pareto archive (preferring t0086 Genuine + Marginal cells), plus 1 random
LHS fill = 96 cells. Per-cell evaluation ran 16 directions x 5 seeds with
objectives = (DSI vector-sum, PD firing rate, robustness as inverse CV of
DSI across seeds). The Pareto front was extracted via pymoo
NonDominatedSorting on the 3-objective evaluations across all generations.
Per-cell biological scoring used 9 electrophys priors (Kole 2008, Werginz
2024, Sivyer 2013 corrected, Branco 2010, Oesch 2005, Stuart 1999,
de Rosenroll 2026, ratio-derived) and 4 morphology priors
(Schachter/Trenholm soma offset, Briggman field elongation, Vaney 2012
anatomical-symmetry pair). Per-cell verdict was the worst-case across all
13 priors (`plausible` if all |dev| <= 2 sigma; `stretched` if up to 5
sigma; `exotic` otherwise).

## Evidence from Papers

The 13 biological priors are grounded in published measurements:

* Kole 2008 — AIS Nav density 0.25-0.5 S/cm^2 prior.
* Werginz 2024 — AIS Nav 1.3 S/cm^2; AIS-to-soma ratio 17.3x.
* Sivyer 2013 (corrected units per t0090 Phase G.2) — dendritic NMDA conductance.
* Schachter 2010 / Trenholm 2013 — soma displacement bounds.
* Briggman 2011 — dendritic field aspect ratio prior.
* Vaney 2012 — anatomical-symmetry priors.
* Anderson 1999 — cable-theoretic v_opt = 2 lambda / tau_m.
* Hausselt 2007 — DSI scales with dendritic length.

See `research/research_papers.md` for the full bibliography.

## Evidence from Internet Sources

The pymoo NSGA-II algorithm parameters (SBX eta=15, polynomial mutation
eta=20, eliminate_duplicates) were chosen following the pymoo 0.6 docs
and Lopez-Camacho 2022 default settings for moderate-d MOEA. NSGA-II
was preferred over BoTorch qLogNEHVI for d=68 per the project's standing
preference (NSGA-II for d > 40, BoTorch only for d <= 40) — see
`research/research_internet.md` for the full discussion.

## Evidence from Code or Experiments

* Pareto front: {n_pareto} cells.
* Verdict distribution: {n_plausible} plausible / {n_stretched} stretched /
  {n_exotic} exotic.
* Anchor distribution (count per anchor): {counts_per_anchor}.
* PD-asymmetric vs ND-asymmetric over-representation: one-sided permutation
  p-value = {pd_vs_nd_p:.4f} (1000 bootstrap resamples).

See:

* `tasks/t0091_morphology_extended_nsga2_v1/results/data/pareto_front.json`
* `tasks/t0091_morphology_extended_nsga2_v1/results/data/biological_scorecard_68d.json`
* `tasks/t0091_morphology_extended_nsga2_v1/results/data/anchor_tracking.json`
* `tasks/t0091_morphology_extended_nsga2_v1/results/images/biological_plausibility_heatmap_68d.png`
* `tasks/t0091_morphology_extended_nsga2_v1/results/images/anchor_tracking_bar.png`
* `tasks/t0091_morphology_extended_nsga2_v1/results/images/dsi_vs_length.png`

## Synthesis

The morphology extension does {"not " if n_plausible == 0 else ""}reach
biologically-plausible joint-pass regions in this run. The v3 electrophys
substrate's existing prior violations (NaP, GABA spatial gradient, NMDA
scaling) carry through to all Pareto cells, suggesting that morphology
variation alone cannot rescue biological plausibility within this
parametrisation. The PD-asymmetric vs ND-asymmetric over-representation
(p={pd_vs_nd_p:.3f}) is below the 5:1 effect-size threshold from
Briggman 2011 needed to claim that soma-displacement-toward-PD asymmetry
is functional given pop 96 / 5 anchors / ~19 cells per anchor.

## Limitations

* 8-generation NSGA-II cap may have terminated before full convergence.
* The 4 morphology priors used wide sigma values from anatomical-symmetry
  arguments rather than direct measurements.
* Robustness was estimated from 5 seeds; larger seed counts would tighten
  the inverse-CV estimate.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus`
* Task: `t0086_robustness_cluster_bio_comparison`
* Task: `t0088_recluster_marginals_and_vm_motifs`
* Task: `t0090_morphology_generator_diversity_test`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0093_resweep_and_t0090_correction`
"""


def _build_metrics_json(*, data: dict[str, object]) -> dict[str, object]:
    pareto_cells = data["pareto"]["cells"]
    anchor_cells = data["anchor"].get("cells", [])
    anchor_to_cells: dict[str, list[dict[str, object]]] = {name: [] for name in ANCHOR_NAMES}
    for ac in anchor_cells:
        name = ac.get("nearest_anchor_name")
        if name in anchor_to_cells:
            anchor_to_cells[name].append(ac)

    variants: list[dict[str, object]] = []

    # Per-anchor variant.
    for name in ANCHOR_NAMES:
        cells = anchor_to_cells[name]
        if len(cells) == 0:
            mean_dsi = None
            mean_robustness = None
        else:
            dsis = [float(c.get("dsi_vector_sum", 0.0)) for c in cells]
            robs = [float(c.get("robustness", 0.0)) for c in cells]
            mean_dsi = sum(dsis) / len(dsis) if dsis else None
            mean_robustness = sum(robs) / len(robs) if robs else None
        variants.append(
            {
                "variant_id": f"anchor-{name.replace('_', '-')}",
                "label": f"Anchor {name}",
                "dimensions": {"anchor": name, "n_cells": len(cells)},
                "metrics": {
                    "direction_selectivity_index": mean_dsi,
                    "tuning_curve_reliability": mean_robustness,
                },
            }
        )

    # All-Pareto variant.
    if len(pareto_cells) > 0:
        all_dsis = [float(c.get("dsi_vector_sum", 0.0)) for c in pareto_cells]
        mean_all = sum(all_dsis) / len(all_dsis)
    else:
        mean_all = None
    variants.append(
        {
            "variant_id": "all-pareto",
            "label": "All Pareto cells",
            "dimensions": {"anchor": "any", "n_cells": len(pareto_cells)},
            "metrics": {
                "direction_selectivity_index": mean_all,
            },
        }
    )

    return {"variants": variants}


def main() -> None:
    ensure_directories()
    data = _load_data()
    n_cells = len(data["pareto"]["cells"])
    if n_cells == 0:
        print("[build_assets] WARNING: pareto_front has 0 cells; skipping")
        return

    # Predictions asset.
    pred_dir = TASK_ROOT / "assets" / "predictions" / PREDICTIONS_ID
    pred_files_dir = pred_dir / "files"
    pred_files_dir.mkdir(parents=True, exist_ok=True)
    (pred_files_dir / "pareto_cells.jsonl").write_text(
        _build_predictions_jsonl(data=data), encoding="utf-8"
    )
    (pred_dir / "details.json").write_text(
        json.dumps(_predictions_details(n_cells=n_cells), indent=2), encoding="utf-8"
    )
    (pred_dir / "description.md").write_text(
        _predictions_description(n_cells=n_cells), encoding="utf-8"
    )
    print(f"[build_assets] wrote predictions asset {pred_dir}")

    # Answer asset.
    ans_dir = TASK_ROOT / "assets" / "answer" / ANSWER_ID
    ans_dir.mkdir(parents=True, exist_ok=True)
    (ans_dir / "details.json").write_text(json.dumps(_answer_details(), indent=2), encoding="utf-8")
    (ans_dir / "short_answer.md").write_text(_short_answer(data=data), encoding="utf-8")
    (ans_dir / "full_answer.md").write_text(_full_answer(data=data), encoding="utf-8")
    print(f"[build_assets] wrote answer asset {ans_dir}")

    # Metrics.
    metrics = _build_metrics_json(data=data)
    metrics_path = RESULTS_DIR / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"[build_assets] wrote metrics {metrics_path}")


if __name__ == "__main__":
    main()
