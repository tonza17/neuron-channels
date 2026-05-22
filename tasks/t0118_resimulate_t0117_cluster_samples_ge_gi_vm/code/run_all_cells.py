"""Top-level driver: iterate the 40-cell manifest, call ``simulate_cell`` sequentially (REQ-10).

Wraps each per-cell call in try/except so a single bad cell does not abort the sweep. Writes any
failures to ``results/data/simulation_failures.csv``. Supports a ``--limit`` flag for pre-flight
runs on a subset of cells.
"""

from __future__ import annotations

import argparse
import time
import traceback

import pandas as pd
from tqdm import tqdm

# Bootstrap NEURON first.
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code import (
    bootstrap as _bootstrap,  # noqa: F401  -- import side effect
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    CLUSTER_ID_COL,
    FAILURE_CELL_KEY_COL,
    FAILURE_DIRECTION_COL,
    FAILURE_ERROR_MESSAGE_COL,
    FAILURE_ERROR_TYPE_COL,
    FAILURE_MODE_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    SEED_COL,
    SOURCE_TASK_COL,
    Direction,
    TrialMode,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.load_t0117_clusters import (
    load_clusters_with_vectors,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    SELECTED_CELLS_CSV,
    SIMULATION_FAILURES_CSV,
    TRACES_ROOT,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.simulate_cell import (
    CellSimResult,
    cell_key,
    simulate_cell,
    trace_parquet_path,
)

_FAILURE_COLUMNS: list[str] = [
    CLUSTER_ID_COL,
    FAILURE_CELL_KEY_COL,
    FAILURE_MODE_COL,
    FAILURE_DIRECTION_COL,
    FAILURE_ERROR_TYPE_COL,
    FAILURE_ERROR_MESSAGE_COL,
]


def _build_cell_rows(*, limit: int | None) -> pd.DataFrame:
    """Read the manifest, join with the 68-d feature vectors, return a DataFrame of cells to run."""
    if not SELECTED_CELLS_CSV.exists():
        raise FileNotFoundError(
            f"Selected-cells manifest missing: {SELECTED_CELLS_CSV}. Run stratified_sample first."
        )
    manifest: pd.DataFrame = pd.read_csv(filepath_or_buffer=SELECTED_CELLS_CSV)
    features: pd.DataFrame = load_clusters_with_vectors()
    key_cols: list[str] = [SOURCE_TASK_COL, SEED_COL, GENERATION_COL, INDIVIDUAL_IDX_COL]
    # Drop duplicated cluster/DSI/PD columns from the features side; manifest is authoritative.
    drop_cols: list[str] = [
        c for c in features.columns if c in manifest.columns and c not in key_cols
    ]
    features_for_join: pd.DataFrame = features.drop(columns=drop_cols)
    joined: pd.DataFrame = pd.merge(
        left=manifest,
        right=features_for_join,
        on=key_cols,
        how="left",
        validate="one_to_one",
    )
    n_missing: int = int(joined["morph_seed"].isna().sum())
    assert n_missing == 0, f"{n_missing} manifest cells failed to resolve in t0117 pooled data"
    if limit is not None and limit > 0:
        # Stratified pre-flight: take one cell per cluster, up to `limit` clusters.
        picked_idx: list[int] = []
        for c in sorted(joined[CLUSTER_ID_COL].unique()):
            cluster_rows: pd.DataFrame = joined.loc[joined[CLUSTER_ID_COL] == c]
            picked_idx.append(int(cluster_rows.index[0]))
            if len(picked_idx) >= limit:
                break
        return joined.loc[picked_idx].copy().reset_index(drop=True)
    return joined.reset_index(drop=True)


def _record_failures_for_trial_errors(
    *,
    result: CellSimResult,
    failures: list[dict[str, str | int]],
) -> None:
    for outcome in result.trials:
        if outcome.success:
            continue
        failures.append(
            {
                CLUSTER_ID_COL: int(result.cluster_id),
                FAILURE_CELL_KEY_COL: result.cell_key,
                FAILURE_MODE_COL: str(outcome.mode.value),
                FAILURE_DIRECTION_COL: int(outcome.direction_deg),
                FAILURE_ERROR_TYPE_COL: outcome.error_type or "Unknown",
                FAILURE_ERROR_MESSAGE_COL: outcome.error_message or "",
            }
        )


def _record_failure_for_cell_build_error(
    *,
    cell_row: pd.Series,
    exc: Exception,
    failures: list[dict[str, str | int]],
) -> None:
    """Single failure row covering an entire cell that could not be built or bundled."""
    key: str = cell_key(
        source_task=str(cell_row[SOURCE_TASK_COL]),
        seed=int(cell_row[SEED_COL]),
        generation=int(cell_row[GENERATION_COL]),
        individual_idx=int(cell_row[INDIVIDUAL_IDX_COL]),
    )
    failures.append(
        {
            CLUSTER_ID_COL: int(cell_row[CLUSTER_ID_COL]),
            FAILURE_CELL_KEY_COL: key,
            FAILURE_MODE_COL: "ALL",
            FAILURE_DIRECTION_COL: -1,
            FAILURE_ERROR_TYPE_COL: type(exc).__name__,
            FAILURE_ERROR_MESSAGE_COL: str(exc),
        }
    )


def run_sweep(*, limit: int | None = None) -> dict[str, int]:
    """Run the per-cell sweep. Returns a summary dict of counts."""
    df_cells: pd.DataFrame = _build_cell_rows(limit=limit)
    TRACES_ROOT.mkdir(parents=True, exist_ok=True)

    failures: list[dict[str, str | int]] = []
    n_cells_done: int = 0
    n_trials_success: int = 0
    n_trials_failure: int = 0
    t_start: float = time.time()

    iterator = tqdm(df_cells.iterrows(), total=len(df_cells), desc="cells")
    for cell_index, row in iterator:
        cell_index_int: int = int(cell_index)  # type: ignore[arg-type]
        cell_t0: float = time.time()
        # Resume support: skip the cell if all 6 trace parquets already exist on disk.
        existing_key: str = cell_key(
            source_task=str(row[SOURCE_TASK_COL]),
            seed=int(row[SEED_COL]),
            generation=int(row[GENERATION_COL]),
            individual_idx=int(row[INDIVIDUAL_IDX_COL]),
        )
        modes_for_check: tuple[TrialMode, ...] = (
            TrialMode.EPSP_PASSIVE,
            TrialMode.IPSP_PASSIVE,
            TrialMode.FULL,
        )
        dirs_for_check: tuple[Direction, ...] = (Direction.PD_DEG, Direction.ND_DEG)
        all_present: bool = all(
            trace_parquet_path(
                traces_root=TRACES_ROOT,
                cluster_id=int(row[CLUSTER_ID_COL]),
                cell_key_str=existing_key,
                mode=m,
                direction_deg=int(d.value),
            ).exists()
            for m in modes_for_check
            for d in dirs_for_check
        )
        if all_present:
            iterator.set_postfix({"cluster": int(row[CLUSTER_ID_COL]), "skipped": "resume"})
            n_trials_success += 6
            n_cells_done += 1
            continue
        try:
            result: CellSimResult = simulate_cell(
                cell_row=row,
                cell_index=cell_index_int,
                traces_root=TRACES_ROOT,
            )
            n_trials_success += result.n_success
            n_trials_failure += result.n_failure
            _record_failures_for_trial_errors(result=result, failures=failures)
            n_cells_done += 1
            cell_dt: float = time.time() - cell_t0
            iterator.set_postfix(
                {
                    "cluster": int(row[CLUSTER_ID_COL]),
                    "ok": result.n_success,
                    "fail": result.n_failure,
                    "dt_s": f"{cell_dt:.1f}",
                }
            )
        except (RuntimeError, ValueError, AssertionError, ArithmeticError, OSError) as exc:
            print(f"cell {cell_index_int} (cluster={int(row[CLUSTER_ID_COL])}) raised: {exc}")
            traceback.print_exc()
            _record_failure_for_cell_build_error(cell_row=row, exc=exc, failures=failures)
            n_trials_failure += 6

    elapsed: float = time.time() - t_start
    print()
    print(f"sweep complete: {n_cells_done}/{len(df_cells)} cells, ")
    print(f"  {n_trials_success} trials succeeded, {n_trials_failure} trials failed")
    print(f"  elapsed: {elapsed:.1f} s ({elapsed / 60.0:.1f} min)")

    # Write failures CSV (always — even if empty, a header-only file is useful for verify_outputs).
    SIMULATION_FAILURES_CSV.parent.mkdir(parents=True, exist_ok=True)
    if len(failures) == 0:
        # Write an empty CSV with the canonical header so the file exists.
        pd.DataFrame(columns=_FAILURE_COLUMNS).to_csv(
            path_or_buf=SIMULATION_FAILURES_CSV, index=False
        )
    else:
        df_failures: pd.DataFrame = pd.DataFrame(failures, columns=_FAILURE_COLUMNS)
        df_failures.to_csv(path_or_buf=SIMULATION_FAILURES_CSV, index=False)
        print(f"wrote {len(df_failures)} failure rows to {SIMULATION_FAILURES_CSV}")

    return {
        "n_cells_done": n_cells_done,
        "n_trials_success": n_trials_success,
        "n_trials_failure": n_trials_failure,
        "n_failure_rows": len(failures),
        "elapsed_s": int(elapsed),
    }


def main() -> None:
    """CLI entry."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Pre-flight: run only the first N cells (one per cluster, raster order).",
    )
    args = parser.parse_args()
    run_sweep(limit=args.limit)


if __name__ == "__main__":
    main()
