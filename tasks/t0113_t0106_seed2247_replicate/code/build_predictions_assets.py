"""Build the three t0104 predictions assets from the synced NSGA-II
evaluation logs.

Each asset captures the per-cell evaluation history of one NSGA-II GA seed
(seed=44, 55, or 66) on the 68-d Bed B + morphology DSGC substrate at
n_obj=2 (DSI vector-sum + PD-rate; robustness dropped from selection per
REQ-2 but the field is still computed by the evaluator and would be in
the predictions if persisted). The script extracts {generation,
vector_68d, dsi_vector_sum, pd_rate_hz, joint_pass} for every evaluated
cell and writes a JSONL file alongside the canonical ``details.json`` and
``description.md`` files required by
``meta/asset_types/predictions/specification.md`` (v2).

Strict joint-pass criterion in t0104 is the 2-axis form: ``DSI >= 0.5
AND PD-rate >= 30 Hz`` on the guard-cleaned DSI (S-0102-01). The
robustness threshold from t0102 is dropped because robustness is no
longer an NSGA-II objective.

Run with
``uv run python -m tasks.t0113_t0106_seed2247_replicate.code.build_predictions_assets``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from tasks.t0113_t0106_seed2247_replicate.code.paths import (
    RESULTS_DATA_DIR,
    TASK_ROOT,
)

# Joint-pass thresholds (t0104 2-objective: DSI + PD-rate only).
JOINT_PASS_DSI_MIN: float = 0.5
JOINT_PASS_PD_RATE_HZ_MIN: float = 30.0

# DSI silence guard threshold (REQ-3; mirrors evaluator.SILENCE_SPIKE_COUNT_THRESHOLD).
DSI_GUARD_SPIKE_COUNT_THRESHOLD: int = 10

# t0104-specific identifiers.
TASK_ID: str = "t0113_t0106_seed2247_replicate"
PROJECT_DATE: str = "2026-05-12"
ASSETS_PREDICTIONS_DIR: Path = TASK_ROOT / "assets" / "predictions"


@dataclass(frozen=True, slots=True)
class SeedConfig:
    seed: int
    predictions_id: str
    all_evaluations_filename: str
    output_jsonl_filename: str


SEED_CONFIGS: list[SeedConfig] = [
    SeedConfig(
        seed=44,
        predictions_id="nsga2-seed44-bedb-morph-n4-gen20-2obj",
        all_evaluations_filename="all_evaluations_seed44.json",
        output_jsonl_filename="predictions-seed44.jsonl",
    ),
    SeedConfig(
        seed=55,
        predictions_id="nsga2-seed55-bedb-morph-n4-gen20-2obj",
        all_evaluations_filename="all_evaluations_seed55.json",
        output_jsonl_filename="predictions-seed55.jsonl",
    ),
    SeedConfig(
        seed=66,
        predictions_id="nsga2-seed66-bedb-morph-n4-gen20-2obj",
        all_evaluations_filename="all_evaluations_seed66.json",
        output_jsonl_filename="predictions-seed66.jsonl",
    ),
]


@dataclass(frozen=True, slots=True)
class SeedSummary:
    seed: int
    predictions_id: str
    n_cells: int
    n_generations_completed: int
    max_dsi: float
    max_pd_rate_hz: float
    n_joint_pass: int
    n_at_guard_floor: int
    hypervolume_final: float
    final_cost_usd: float


def _is_joint_pass(*, dsi: float, pd_rate_hz: float) -> bool:
    return dsi >= JOINT_PASS_DSI_MIN and pd_rate_hz >= JOINT_PASS_PD_RATE_HZ_MIN


def _read_json(*, path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _extract_records(*, all_evals_path: Path) -> list[dict[str, object]]:
    raw = _read_json(path=all_evals_path)
    assert isinstance(raw, dict), f"expected dict in {all_evals_path}"
    evaluations = raw.get("evaluations")
    assert isinstance(evaluations, list), f"expected 'evaluations' list in {all_evals_path}"
    records: list[dict[str, object]] = []
    for entry in evaluations:
        assert isinstance(entry, dict)
        dsi = float(entry["dsi_vector_sum"])
        pd_rate = float(entry["pd_rate_hz"])
        records.append(
            {
                "generation": int(entry["generation"]),
                "vector_68d": list(entry["vector_68d"]),
                "dsi_vector_sum": dsi,
                "pd_rate_hz": pd_rate,
                "joint_pass": _is_joint_pass(dsi=dsi, pd_rate_hz=pd_rate),
            }
        )
    return records


def _final_hypervolume(*, hv_traj_path: Path) -> float:
    raw = _read_json(path=hv_traj_path)
    assert isinstance(raw, dict)
    traj = raw.get("trajectory")
    assert isinstance(traj, list) and len(traj) > 0
    last = traj[-1]
    assert isinstance(last, dict)
    return float(last["hypervolume"])


def _final_cost(*, hv_traj_path: Path) -> float:
    raw = _read_json(path=hv_traj_path)
    assert isinstance(raw, dict)
    traj = raw.get("trajectory")
    assert isinstance(traj, list) and len(traj) > 0
    last = traj[-1]
    assert isinstance(last, dict)
    return float(last["cumulative_cost_usd"])


def _summarise(
    *,
    seed: int,
    predictions_id: str,
    records: list[dict[str, object]],
    hv_final: float,
    cost: float,
) -> SeedSummary:
    n_cells = len(records)
    n_gens: int = max(
        (int(r["generation"]) for r in records if isinstance(r["generation"], int)),
        default=0,
    )
    max_dsi: float = max(
        (
            float(r["dsi_vector_sum"])
            for r in records
            if isinstance(r["dsi_vector_sum"], int | float)
        ),
        default=0.0,
    )
    max_pd: float = max(
        (float(r["pd_rate_hz"]) for r in records if isinstance(r["pd_rate_hz"], int | float)),
        default=0.0,
    )
    n_jp = sum(1 for r in records if bool(r["joint_pass"]))
    # Cells at the DSI guard floor (DSI == 0.0 because total spikes <
    # threshold). The recorded DSI is the guard-cleaned value, so any 0.0
    # is a candidate floor cell; we treat exact-zero as the floor.
    n_floor = sum(
        1
        for r in records
        if isinstance(r["dsi_vector_sum"], int | float) and float(r["dsi_vector_sum"]) == 0.0
    )
    return SeedSummary(
        seed=seed,
        predictions_id=predictions_id,
        n_cells=n_cells,
        n_generations_completed=n_gens,
        max_dsi=max_dsi,
        max_pd_rate_hz=max_pd,
        n_joint_pass=n_jp,
        n_at_guard_floor=n_floor,
        hypervolume_final=hv_final,
        final_cost_usd=cost,
    )


def _write_jsonl(*, records: list[dict[str, object]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record))
            handle.write("\n")


def _write_details_json(*, summary: SeedSummary, asset_dir: Path, jsonl_filename: str) -> None:
    details = {
        "spec_version": "2",
        "predictions_id": summary.predictions_id,
        "name": (
            f"NSGA-II seed={summary.seed} Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 "
            "(LHS random init, 2-objective DSI+PD, DSI silence guard)"
        ),
        "short_description": (
            f"All per-cell NSGA-II evaluations from t0104 random-init seed={summary.seed} "
            f"({summary.n_cells} cells across {summary.n_generations_completed} generations) "
            "on the 68-d Bed B + morphology DSGC substrate at N_EVAL_SEEDS=4, n_obj=2 "
            "(DSI + PD-rate; robustness dropped from selection per REQ-2). The DSI "
            "silence guard from S-0102-01 is active: cells with total mean spikes "
            "across the 16 directions below 10 are forced to DSI = 0.0."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "Compartmental DSGC neuron model with the t0092-patched procedural morphology "
            "generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys "
            "parameter vector applied via t0080's apply_parameter_vector. Each cell is "
            "evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises "
            "the negated pair (DSI vector-sum, PD-rate) — robustness is computed per cell "
            "but does NOT enter NSGA-II selection in t0104 (REQ-2). The DSI silence guard "
            "(REQ-3) clamps DSI to 0.0 when the cell's total mean spikes across directions "
            "fall below 10, eliminating the t0102 silence-corner artifact."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl",
        "prediction_schema": (
            "Each line is a JSON object with fields: generation (int, NSGA-II generation "
            "this cell was evaluated at; 1 = initial LHS population), vector_68d (list of 68 "
            "floats, the 54-d electrophys + 14-d morphology parameter vector), "
            "dsi_vector_sum (float in [0, 1], vector-sum direction selectivity index; "
            "guard-cleaned per REQ-3 so values of 0.0 may either be real or guard-floor), "
            "pd_rate_hz (float, preferred-direction mean firing rate in Hz), joint_pass "
            "(bool, true iff dsi_vector_sum >= 0.5 AND pd_rate_hz >= 30 — the t0104 "
            "2-axis strict criterion)."
        ),
        "instance_count": summary.n_cells,
        "metrics_at_creation": {
            "n_generations_completed": summary.n_generations_completed,
            "n_cells": summary.n_cells,
            "max_dsi": summary.max_dsi,
            "max_pd_rate_hz": summary.max_pd_rate_hz,
            "n_joint_pass": summary.n_joint_pass,
            "n_at_guard_floor": summary.n_at_guard_floor,
            "hypervolume_final": summary.hypervolume_final,
            "final_cost_usd": summary.final_cost_usd,
        },
        "files": [
            {
                "path": f"files/{jsonl_filename}",
                "description": (
                    f"Per-cell NSGA-II evaluation log for t0104 seed={summary.seed} "
                    f"({summary.n_cells} cells)."
                ),
                "format": "jsonl",
            }
        ],
        "categories": [
            "direction-selectivity",
            "compartmental-modeling",
            "retinal-ganglion-cell",
            "dendritic-computation",
        ],
        "source_paper_ids": [],
        "source_task_ids": [
            "t0024_port_de_rosenroll_2026_dsgc",
            "t0080_bedb_mobo_v3_dendritic_spike_nsga2",
            "t0090_morphology_generator_diversity_test",
            "t0091_morphology_extended_nsga2_v1",
            "t0092_diagnose_morphology_generator_silence",
            "t0093_resweep_and_t0090_correction",
            "t0099_random_init_pareto_robustness",
            "t0102_seedscale_n4_gen20",
        ],
        "created_by_task": TASK_ID,
        "date_created": PROJECT_DATE,
    }
    details_path = asset_dir / "details.json"
    with details_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(details, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def _write_description_md(*, summary: SeedSummary, asset_dir: Path, jsonl_filename: str) -> None:
    body = _description_body(
        summary=summary,
        jsonl_filename=jsonl_filename,
    )
    desc_path = asset_dir / "description.md"
    with desc_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(body)


def _description_body(*, summary: SeedSummary, jsonl_filename: str) -> str:
    name = (
        f"NSGA-II seed={summary.seed} Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 "
        "(LHS random init, 2-objective DSI+PD, DSI silence guard)"
    )
    metadata = (
        "## Metadata\n\n"
        f"* **Name**: {name}\n"
        "* **Model**: DSGC compartmental model (t0092-patched procedural morphology "
        "+ 54-d Bed B electrophys vector via t0080 apply_params)\n"
        "* **Datasets**: none (simulator outputs)\n"
        "* **Format**: jsonl\n"
        f"* **Instances**: {summary.n_cells:,} per-cell evaluations across "
        f"{summary.n_generations_completed} NSGA-II generations\n"
        f"* **Created by**: {TASK_ID}\n"
    )
    overview = (
        "## Overview\n\n"
        f"This predictions asset records every cell evaluated by the t0104 NSGA-II "
        f"run with GA seed={summary.seed}. The run is one of three independent "
        "random-init restarts (44, 55, 66) that test whether dropping the "
        "robustness axis from NSGA-II's objective vector (3 -> 2) and applying "
        "the DSI silence guard (S-0102-01) recover joint-pass cells where "
        "t0102's 3-objective N=4 run found zero across 2,592 cells.\n\n"
        "Each line of the JSONL captures one DSGC compartmental simulation: "
        "the 68-d parameter vector (54 electrophys knobs + 14 morphology "
        "knobs), the two NSGA-II objectives (DSI vector-sum and "
        "preferred-direction firing rate), and a precomputed strict 2-axis "
        "joint-pass flag (DSI >= 0.5 AND PD >= 30 Hz). Robustness is computed "
        "internally per cell by the evaluator but is not persisted to this "
        "JSONL because it is no longer an NSGA-II objective in t0104.\n\n"
        f"The seed terminated at generation {summary.n_generations_completed} "
        f"(either at the planned 20 cap or earlier via the cost watchdog at "
        f"$4.00 per seed); final hypervolume in the 2-D (DSI, PD) plane was "
        f"{summary.hypervolume_final:.4f} and final cost "
        f"${summary.final_cost_usd:.4f}.\n"
    )
    model_section = (
        "## Model\n\n"
        "DSGC compartmental neuron model with the t0092-patched procedural "
        "morphology generator (``generate_fixed_morphology``, canonical via "
        "correction C-0093-01) and the 54-d Bed B electrophys parameter vector "
        "applied via t0080's ``apply_parameter_vector``. Per-cell evaluation "
        "runs 16 stimulus directions x 4 noise replicates with objectives = "
        "(DSI vector-sum, preferred-direction firing rate in Hz), both "
        "maximised. Pymoo NSGA-II minimises the negated pair. Crossover SBX "
        "eta=15 with prob=0.9; polynomial mutation eta=20 with prob=1/68; "
        "elimination of duplicates enabled. Population size 96, max "
        "generations 20, LHS-initialised initial population with explicit "
        "``np.random.SeedSequence`` seeding for reproducibility. The DSI "
        "silence guard (REQ-3) is active: cells whose total mean spike count "
        f"across the 16 directions falls below "
        f"{DSI_GUARD_SPIKE_COUNT_THRESHOLD} have DSI clamped to 0.0 "
        "before being returned to NSGA-II.\n"
    )
    data_section = (
        "## Data\n\n"
        "No external dataset is consumed. Input vectors are 68-d points "
        "sampled by NSGA-II starting from a 96-row Latin Hypercube Sample "
        "drawn with pymoo's ``LatinHypercubeSampling`` and explicitly seeded "
        f"with task_seed={summary.seed}. Bounds for the 68 parameters are "
        "inherited unchanged from the t0102 / t0099 substrate (the same 54-d "
        "electrophys bounds from t0080 plus the 14-d morphology bounds from "
        "t0090). Noise replicates inside each evaluation use the four "
        "deterministically spawned RNG seeds drawn from "
        "``np.random.SeedSequence(42).spawn(5)``.\n"
    )
    prediction_format_section = (
        "## Prediction Format\n\n"
        f"JSONL with one line per evaluated cell ({summary.n_cells:,} lines "
        "total). Each line is a JSON object with fields:\n\n"
        "* ``generation``: int, the NSGA-II generation at which this cell was "
        "evaluated (1 = initial LHS population, 2..N = offspring generations)\n"
        "* ``vector_68d``: list of 68 floats, the 54-d electrophys + 14-d "
        "morphology parameter vector\n"
        "* ``dsi_vector_sum``: float in [0, 1], vector-sum direction "
        "selectivity index averaged across the 4 noise replicates "
        f"(guard-cleaned per REQ-3 at threshold "
        f"{DSI_GUARD_SPIKE_COUNT_THRESHOLD})\n"
        "* ``pd_rate_hz``: float, preferred-direction mean firing rate in Hz "
        "(mean across the 4 replicates)\n"
        "* ``joint_pass``: bool, true iff ``dsi_vector_sum >= 0.5`` AND "
        "``pd_rate_hz >= 30`` (the t0104 strict 2-axis "
        "biological-plausibility corner; t0102's robustness >= 0.7 "
        "threshold is dropped because robustness is no longer an NSGA-II "
        "objective)\n\n"
        "Example line (formatted for readability):\n\n"
        "```\n"
        "{\n"
        '  "generation": 14,\n'
        '  "vector_68d": [0.4576, 0.0550, ..., 0.2229],\n'
        '  "dsi_vector_sum": 0.4321,\n'
        '  "pd_rate_hz": 22.43,\n'
        '  "joint_pass": false\n'
        "}\n"
        "```\n"
    )
    metrics_section = (
        "## Metrics\n\n"
        "Headline metrics computed at asset creation time:\n\n"
        "| Metric | Value |\n"
        "|--------|-------|\n"
        f"| Cells evaluated | **{summary.n_cells:,}** |\n"
        f"| Generations completed | **{summary.n_generations_completed}** / 20 |\n"
        f"| Best DSI (vector sum, guard-cleaned) | **{summary.max_dsi:.4f}** |\n"
        f"| Best preferred-direction rate (Hz) | **{summary.max_pd_rate_hz:.2f}** |\n"
        f"| Strict joint-pass cells (DSI >= 0.5 AND PD >= 30) | **{summary.n_joint_pass}** |\n"
        f"| Cells at DSI guard floor (DSI = 0.0) | **{summary.n_at_guard_floor}** |\n"
        f"| Final hypervolume (2-D) | **{summary.hypervolume_final:.4f}** |\n"
        f"| Final NSGA-II compute cost (USD) | **${summary.final_cost_usd:.4f}** |\n\n"
        "The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 "
        f"Hz) is met by **{summary.n_joint_pass}** of the "
        f"{summary.n_cells:,} evaluated cells.\n"
    )
    main_ideas_section = (
        "## Main Ideas\n\n"
        f"* The run terminated at generation {summary.n_generations_completed} "
        "(either at the planned cap of 20 or earlier via the per-seed cost "
        "watchdog at $4.00). Per-cell wall-clock at N_EVAL_SEEDS=4 was the "
        "operative throughput constant; the predictions JSONL captures every "
        "evaluation up to the termination point.\n"
        f"* {summary.n_joint_pass} of the {summary.n_cells:,} evaluated cells "
        "cleared the strict 2-axis joint-pass corner (DSI >= 0.5 AND PD >= 30 "
        f"Hz). Best per-axis maxima are DSI={summary.max_dsi:.4f} and "
        f"PD-rate={summary.max_pd_rate_hz:.2f} Hz on the guard-cleaned DSI.\n"
        f"* {summary.n_at_guard_floor} of the {summary.n_cells:,} cells are "
        "at the DSI guard floor (DSI = 0.0 because total mean spikes < "
        f"{DSI_GUARD_SPIKE_COUNT_THRESHOLD}); these are the cells that would "
        "have produced the t0102 silence-corner artifact at DSI = 1.0 without "
        "the guard. Per-cell ``vector_68d`` is sufficient to re-evaluate any "
        "cell without re-running the optimiser.\n"
    )
    summary_section = (
        "## Summary\n\n"
        f"This asset captures all {summary.n_cells:,} NSGA-II evaluations from "
        f"the t0104 random-init 2-objective run with GA seed={summary.seed}, "
        f"covering generations 1 through {summary.n_generations_completed}. "
        "Each cell is a 68-d point in the Bed B electrophys + procedural "
        "morphology parameter space, evaluated with 16 stimulus directions "
        "and 4 noise replicates against the 2-dimensional objective (DSI "
        "vector-sum, preferred-direction firing rate). The DSI silence guard "
        "from S-0102-01 is active throughout.\n\n"
        f"The headline finding for this seed is that {summary.n_joint_pass} "
        "of the evaluated cells cleared the strict 2-axis joint-pass corner. "
        f"Best individual axes were DSI={summary.max_dsi:.4f} and "
        f"PD={summary.max_pd_rate_hz:.2f} Hz. Combined with the matched "
        "two-other-seed assets in t0104 and the t0102 three-objective prior, "
        "this contributes one of three apples-to-apples comparisons of the "
        "2-objective vs 3-objective NSGA-II formulations on the same "
        "substrate.\n\n"
        f"The asset is a primary evidence channel for the t0104 answer asset. "
        f"Cost watchdog and HV-plateau termination jointly govern run length; "
        f"the final cost reading was ${summary.final_cost_usd:.4f} and the "
        f"run reached generation {summary.n_generations_completed} of the "
        "planned 20.\n"
    )
    return (
        "---\n"
        f'spec_version: "2"\n'
        f'predictions_id: "{summary.predictions_id}"\n'
        f'documented_by_task: "{TASK_ID}"\n'
        f'date_documented: "{PROJECT_DATE}"\n'
        "---\n\n"
        f"# {name}\n\n"
        f"{metadata}\n"
        f"{overview}\n"
        f"{model_section}\n"
        f"{data_section}\n"
        f"{prediction_format_section}\n"
        f"{metrics_section}\n"
        f"{main_ideas_section}\n"
        f"{summary_section}"
    )


def _build_one(*, config: SeedConfig) -> SeedSummary:
    all_evals_path = RESULTS_DATA_DIR / config.all_evaluations_filename
    hv_traj_path = RESULTS_DATA_DIR / f"hv_trajectory_seed{config.seed}.json"
    records = _extract_records(all_evals_path=all_evals_path)
    hv_final = _final_hypervolume(hv_traj_path=hv_traj_path)
    cost = _final_cost(hv_traj_path=hv_traj_path)
    summary = _summarise(
        seed=config.seed,
        predictions_id=config.predictions_id,
        records=records,
        hv_final=hv_final,
        cost=cost,
    )
    asset_dir = ASSETS_PREDICTIONS_DIR / config.predictions_id
    asset_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = asset_dir / "files" / config.output_jsonl_filename
    _write_jsonl(records=records, out_path=jsonl_path)
    _write_details_json(
        summary=summary,
        asset_dir=asset_dir,
        jsonl_filename=config.output_jsonl_filename,
    )
    _write_description_md(
        summary=summary,
        asset_dir=asset_dir,
        jsonl_filename=config.output_jsonl_filename,
    )
    return summary


def main() -> None:
    print(f"[build_predictions_assets] start at {datetime.now(UTC).isoformat()}")
    summaries: list[SeedSummary] = []
    for config in SEED_CONFIGS:
        if not (RESULTS_DATA_DIR / config.all_evaluations_filename).exists():
            print(
                f"[build_predictions_assets] skipping seed={config.seed} — "
                f"{config.all_evaluations_filename} not present"
            )
            continue
        summary = _build_one(config=config)
        summaries.append(summary)
        print(
            f"[build_predictions_assets] seed={summary.seed} "
            f"id={summary.predictions_id} cells={summary.n_cells} "
            f"gens={summary.n_generations_completed} "
            f"max_dsi={summary.max_dsi:.4f} max_pd={summary.max_pd_rate_hz:.2f} "
            f"joint_pass={summary.n_joint_pass} "
            f"floor={summary.n_at_guard_floor} "
            f"hv_final={summary.hypervolume_final:.4f} "
            f"cost=${summary.final_cost_usd:.4f}"
        )
    total_jp = sum(s.n_joint_pass for s in summaries)
    print(f"[build_predictions_assets] DONE. total_joint_pass={total_jp}")


if __name__ == "__main__":
    main()
