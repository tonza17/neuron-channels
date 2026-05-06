"""Phase A: re-evaluate 20 cells x 5 replications using evaluate_parameter_vector.

For each cell and each of 5 outer RNG seeds:
* monkey-patch t0080.trial_driver.SEED_BASE = seed
* call evaluate_parameter_vector with 24 directions (every 15 deg) x 30 seeds
* record dsi, pd_rate_hz, peak_vm_mv, is_unstable, elapsed_s, parameter_hash
* append to results/data/replication_results.json after each call (resumable)
* check cost watchdog after each cell-eval; trip if cost >= $3.50

CLI:
    uv run python -m tasks.t0086_robustness_cluster_bio_comparison.code.run_phase_a \\
        --all-cells --max-workers 43

    uv run python -m tasks.t0086_robustness_cluster_bio_comparison.code.run_phase_a \\
        --smoke-only --cell-id 767 --seeds-only 1 --max-workers 43
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import trial_driver as t80_trial
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParameterVector
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    evaluate_parameter_vector,
)
from tasks.t0086_robustness_cluster_bio_comparison.code.cost_watchdog import (
    T0086_HARD_BUDGET_USD,
    make_watchdog_from_machine_log,
    patch_t0080_loop_rate,
)
from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    BUDGET_OVERRUN_MD,
    MACHINE_LOG_JSON,
    REPLICATION_RESULTS_JSON,
    REPLICATION_SEEDS_JSON,
    SELECTED_CELLS_JSON,
    ensure_directories,
)

ANGLES_24DIR_DEG: tuple[int, ...] = tuple(range(0, 360, 15))
N_INNER_SEEDS: int = 30


@dataclass(frozen=True, slots=True)
class ReplicationRecord:
    cell_id: int
    selection_reason: str
    seed_index: int
    seed: int
    parameter_hash: str
    dsi: float
    pd_rate_hz: float
    peak_vm_mv: float
    is_unstable: bool
    elapsed_s: float
    timestamp: str


def _hash_params(params: list[float]) -> str:
    raw = ",".join(f"{v:.18e}" for v in params)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _load_existing_results() -> list[ReplicationRecord]:
    if not REPLICATION_RESULTS_JSON.exists():
        return []
    raw = json.loads(REPLICATION_RESULTS_JSON.read_text(encoding="utf-8"))
    records: list[dict[str, object]] = raw["records"] if isinstance(raw, dict) else raw
    return [
        ReplicationRecord(
            cell_id=int(r["cell_id"]),  # type: ignore[arg-type]
            selection_reason=str(r["selection_reason"]),
            seed_index=int(r["seed_index"]),  # type: ignore[arg-type]
            seed=int(r["seed"]),  # type: ignore[arg-type]
            parameter_hash=str(r["parameter_hash"]),
            dsi=float(r["dsi"]),  # type: ignore[arg-type]
            pd_rate_hz=float(r["pd_rate_hz"]),  # type: ignore[arg-type]
            peak_vm_mv=float(r["peak_vm_mv"]),  # type: ignore[arg-type]
            is_unstable=bool(r["is_unstable"]),
            elapsed_s=float(r["elapsed_s"]),  # type: ignore[arg-type]
            timestamp=str(r["timestamp"]),
        )
        for r in records
    ]


def _save_results(*, records: list[ReplicationRecord]) -> None:
    payload = {
        "n_records": len(records),
        "records": [asdict(r) for r in records],
    }
    REPLICATION_RESULTS_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _completed_pairs(records: list[ReplicationRecord]) -> set[tuple[int, int]]:
    return {(r.cell_id, r.seed_index) for r in records}


def _run_one_replication(
    *,
    cell_id: int,
    selection_reason: str,
    params_list: list[float],
    seed_index: int,
    seed: int,
    angles_deg: tuple[int, ...],
    n_inner_seeds: int,
    max_workers: int,
) -> ReplicationRecord:
    t80_trial.SEED_BASE = seed  # type: ignore[attr-defined]
    pv = ParameterVector(values=np.asarray(params_list, dtype=np.float64))
    t0 = time.time()
    eval_res = evaluate_parameter_vector(
        params=pv,
        angles_deg=angles_deg,
        n_seeds=n_inner_seeds,
        max_workers=max_workers,
    )
    elapsed = time.time() - t0
    return ReplicationRecord(
        cell_id=cell_id,
        selection_reason=selection_reason,
        seed_index=seed_index,
        seed=seed,
        parameter_hash=_hash_params(params_list),
        dsi=float(eval_res.dsi),
        pd_rate_hz=float(eval_res.pd_rate_hz),
        peak_vm_mv=float(eval_res.peak_vm_mv),
        is_unstable=bool(eval_res.is_unstable),
        elapsed_s=elapsed,
        timestamp=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def run_phase_a(
    *,
    smoke_only: bool,
    cell_id_filter: int | None,
    seeds_only: int | None,
    max_workers: int,
    angles_deg: tuple[int, ...] = ANGLES_24DIR_DEG,
    n_inner_seeds: int = N_INNER_SEEDS,
    hard_budget_usd: float = T0086_HARD_BUDGET_USD,
) -> None:
    ensure_directories()
    selected = json.loads(SELECTED_CELLS_JSON.read_text(encoding="utf-8"))
    seeds_payload = json.loads(REPLICATION_SEEDS_JSON.read_text(encoding="utf-8"))
    seeds: list[int] = list(seeds_payload["seeds"])
    if seeds_only is not None:
        seeds = seeds[:seeds_only]

    cells_to_run: list[dict[str, object]] = list(selected["joint_pass_cells"]) + list(
        selected["near_pass_cells"]
    )
    if cell_id_filter is not None:
        cells_to_run = [c for c in cells_to_run if int(c["cell_index"]) == cell_id_filter]
    if smoke_only and len(cells_to_run) > 0:
        cells_to_run = [cells_to_run[0]]

    print(
        f"[run_phase_a] starting: cells={len(cells_to_run)} seeds={len(seeds)} "
        f"angles={len(angles_deg)} inner_seeds={n_inner_seeds} "
        f"max_workers={max_workers} hard_budget=${hard_budget_usd:.2f}",
        flush=True,
    )

    instance_started_at = datetime.now(UTC)
    watchdog = make_watchdog_from_machine_log(
        machine_log_path=MACHINE_LOG_JSON,
        instance_started_at=instance_started_at,
        hard_budget_usd=hard_budget_usd,
    )
    patch_t0080_loop_rate(rate=watchdog.hourly_rate_usd)

    records: list[ReplicationRecord] = _load_existing_results()
    completed = _completed_pairs(records)
    print(f"[run_phase_a] resuming from {len(records)} existing records", flush=True)

    n_total = len(cells_to_run) * len(seeds)
    n_done = 0
    for cell in cells_to_run:
        cell_id: int = int(cell["cell_index"])  # type: ignore[arg-type]
        selection_reason: str = str(cell["selection_reason"])
        params_list: list[float] = [float(v) for v in cell["params"]]  # type: ignore[union-attr]
        for seed_index, seed in enumerate(seeds):
            n_done += 1
            if (cell_id, seed_index) in completed:
                print(
                    f"[run_phase_a] [{n_done}/{n_total}] cell {cell_id} "
                    f"seed_index {seed_index} already done; skipping",
                    flush=True,
                )
                continue
            if watchdog.trip_if_over_cap(intervention_md_path=BUDGET_OVERRUN_MD):
                print(
                    f"[run_phase_a] BUDGET CAP HIT (${watchdog.current_cost_usd():.4f} >= "
                    f"${hard_budget_usd:.2f}); halting after {len(records)} records",
                    flush=True,
                )
                _save_results(records=records)
                return
            print(
                f"[run_phase_a] [{n_done}/{n_total}] cell {cell_id} ({selection_reason}) "
                f"seed_index={seed_index} seed={seed} "
                f"cost=${watchdog.current_cost_usd():.4f}",
                flush=True,
            )
            rec = _run_one_replication(
                cell_id=cell_id,
                selection_reason=selection_reason,
                params_list=params_list,
                seed_index=seed_index,
                seed=seed,
                angles_deg=angles_deg,
                n_inner_seeds=n_inner_seeds,
                max_workers=max_workers,
            )
            print(
                f"[run_phase_a]    -> dsi={rec.dsi:.3f} pd={rec.pd_rate_hz:.2f}Hz "
                f"unstable={rec.is_unstable} elapsed={rec.elapsed_s:.1f}s "
                f"hash={rec.parameter_hash}",
                flush=True,
            )
            records.append(rec)
            _save_results(records=records)

    print(
        f"[run_phase_a] completed: {len(records)} total records; "
        f"final cost=${watchdog.current_cost_usd():.4f}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase A robustness re-evaluation")
    parser.add_argument("--all-cells", action="store_true", help="Run all 20 cells x all seeds")
    parser.add_argument(
        "--smoke-only",
        action="store_true",
        help="Run only one cell at one seed (smoke gate before full sweep)",
    )
    parser.add_argument(
        "--cell-id",
        type=int,
        default=None,
        help="If set, restrict to this cell_index only",
    )
    parser.add_argument(
        "--seeds-only",
        type=int,
        default=None,
        help="If set, use only the first N seeds",
    )
    parser.add_argument("--max-workers", type=int, default=43)
    parser.add_argument("--hard-budget-usd", type=float, default=T0086_HARD_BUDGET_USD)
    args = parser.parse_args()
    if not (args.all_cells or args.smoke_only):
        parser.error("must pass --all-cells or --smoke-only")
    run_phase_a(
        smoke_only=args.smoke_only,
        cell_id_filter=args.cell_id,
        seeds_only=args.seeds_only,
        max_workers=args.max_workers,
        hard_budget_usd=args.hard_budget_usd,
    )


if __name__ == "__main__":
    main()
