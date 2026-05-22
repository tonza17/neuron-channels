"""Manifest-resolution + trace-parquet verification (REQ-15).

Checks:
1. selected_cells.csv has exactly 40 rows (10 per cluster), unique primary keys, each resolving to
   exactly one row of t0117 pooled_all_cells.parquet.
2. For every (cell, mode, direction) triple, EITHER the canonical-path parquet exists AND has
   exactly 1400 rows AND the correct mode-specific columns, OR a matching row is present in
   simulation_failures.csv.
3. For every existing parquet, the recorded columns match the mode contract:
   EPSP_PASSIVE -> {t_ms, g_e_us}; IPSP_PASSIVE -> {t_ms, g_i_us}; FULL -> {t_ms, v_m_mv}.

Exits 0 if every check passes, 1 otherwise.
"""

from __future__ import annotations

import sys

import pandas as pd

from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    CLUSTER_ID_COL,
    EXPECTED_TRACE_ROWS,
    FAILURE_CELL_KEY_COL,
    FAILURE_DIRECTION_COL,
    FAILURE_MODE_COL,
    G_E_US_COL,
    G_I_US_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    N_CELLS_PER_CLUSTER,
    N_CLUSTERS,
    N_SELECTED_CELLS_TOTAL,
    SEED_COL,
    SOURCE_TASK_COL,
    T_MS_COL,
    V_M_MV_COL,
    Direction,
    TrialMode,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    SELECTED_CELLS_CSV,
    SIMULATION_FAILURES_CSV,
    T0117_POOLED_PARQUET,
    TRACES_ROOT,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.simulate_cell import (
    cell_key,
    trace_parquet_path,
)

_EXPECTED_COLUMNS_BY_MODE: dict[TrialMode, set[str]] = {
    TrialMode.EPSP_PASSIVE: {T_MS_COL, G_E_US_COL},
    TrialMode.IPSP_PASSIVE: {T_MS_COL, G_I_US_COL},
    TrialMode.FULL: {T_MS_COL, V_M_MV_COL},
}


def _check_manifest() -> tuple[pd.DataFrame, list[str]]:
    """Load the manifest and run the row-count / uniqueness / resolution checks."""
    errors: list[str] = []
    manifest: pd.DataFrame = pd.read_csv(filepath_or_buffer=SELECTED_CELLS_CSV)
    if len(manifest) != N_SELECTED_CELLS_TOTAL:
        errors.append(f"manifest has {len(manifest)} rows, expected {N_SELECTED_CELLS_TOTAL}")
    for c in range(N_CLUSTERS):
        n_c: int = int((manifest[CLUSTER_ID_COL] == c).sum())
        if n_c != N_CELLS_PER_CLUSTER:
            errors.append(f"cluster {c}: {n_c} rows (expected {N_CELLS_PER_CLUSTER})")
    key_cols: list[str] = [SOURCE_TASK_COL, SEED_COL, GENERATION_COL, INDIVIDUAL_IDX_COL]
    n_unique: int = manifest.groupby(key_cols).ngroups
    if n_unique != len(manifest):
        errors.append(
            f"manifest primary key not unique: {n_unique} unique tuples for {len(manifest)} rows"
        )

    # Manifest must resolve to t0117 pooled_all_cells.parquet.
    pooled: pd.DataFrame = pd.read_parquet(path=T0117_POOLED_PARQUET)
    merged = pd.merge(
        left=manifest,
        right=pooled[key_cols],
        on=key_cols,
        how="left",
        indicator=True,
    )
    n_missing: int = int((merged["_merge"] == "left_only").sum())
    if n_missing > 0:
        errors.append(f"{n_missing} manifest rows did not resolve in t0117 pooled parquet")
    return manifest, errors


def _check_trace_parquets(*, manifest: pd.DataFrame) -> list[str]:
    """For every (cell, mode, direction), verify the parquet OR a matching failure row exists."""
    errors: list[str] = []
    if SIMULATION_FAILURES_CSV.exists():
        failures: pd.DataFrame = pd.read_csv(filepath_or_buffer=SIMULATION_FAILURES_CSV)
    else:
        failures = pd.DataFrame(
            columns=[
                CLUSTER_ID_COL,
                FAILURE_CELL_KEY_COL,
                FAILURE_MODE_COL,
                FAILURE_DIRECTION_COL,
            ]
        )

    modes: tuple[TrialMode, ...] = (
        TrialMode.EPSP_PASSIVE,
        TrialMode.IPSP_PASSIVE,
        TrialMode.FULL,
    )
    directions: tuple[Direction, ...] = (Direction.PD_DEG, Direction.ND_DEG)

    for _idx, row in manifest.iterrows():
        cluster_id: int = int(row[CLUSTER_ID_COL])
        key: str = cell_key(
            source_task=str(row[SOURCE_TASK_COL]),
            seed=int(row[SEED_COL]),
            generation=int(row[GENERATION_COL]),
            individual_idx=int(row[INDIVIDUAL_IDX_COL]),
        )
        for mode in modes:
            for direction in directions:
                d_deg: int = int(direction.value)
                path = trace_parquet_path(
                    traces_root=TRACES_ROOT,
                    cluster_id=cluster_id,
                    cell_key_str=key,
                    mode=mode,
                    direction_deg=d_deg,
                )
                if path.exists():
                    df: pd.DataFrame = pd.read_parquet(path=path)
                    if len(df) != EXPECTED_TRACE_ROWS:
                        errors.append(f"{path} has {len(df)} rows (expected {EXPECTED_TRACE_ROWS})")
                    expected_cols: set[str] = _EXPECTED_COLUMNS_BY_MODE[mode]
                    have_cols: set[str] = set(df.columns)
                    if have_cols != expected_cols:
                        msg: str = (
                            f"{path} columns {sorted(have_cols)} != "
                            f"expected {sorted(expected_cols)}"
                        )
                        errors.append(msg)
                else:
                    # Must be matched by a failure row covering this cell, mode, direction.
                    mask = (
                        (failures.get(CLUSTER_ID_COL) == cluster_id)
                        & (failures.get(FAILURE_CELL_KEY_COL) == key)
                        & (
                            (failures.get(FAILURE_MODE_COL) == mode.value)
                            | (failures.get(FAILURE_MODE_COL) == "ALL")
                        )
                        & (
                            (failures.get(FAILURE_DIRECTION_COL) == d_deg)
                            | (failures.get(FAILURE_DIRECTION_COL) == -1)
                        )
                    )
                    if not bool(mask.any()):
                        errors.append(
                            f"missing trace at {path} and no matching simulation_failures row"
                        )
    return errors


def verify() -> int:
    """Run all checks. Returns 0 on success, 1 if any check failed."""
    manifest, errors = _check_manifest()
    errors.extend(_check_trace_parquets(manifest=manifest))
    if len(errors) == 0:
        print("verify_outputs: all checks passed")
        return 0
    print(f"verify_outputs: {len(errors)} check(s) failed")
    for e in errors:
        print(f"  - {e}")
    return 1


def main() -> None:
    """CLI entry."""
    sys.exit(verify())


if __name__ == "__main__":
    main()
