"""Quality sanity check: for every cell with DSI > 0.5, PD spikes > ND spikes (REQ-14).

Reads ``per_cell_metrics.csv`` and ``selected_cells.csv``, pivots to one row per cell with PD and
ND spike counts, computes per-cell pass/fail, writes ``results/data/dsi_sanity_check.csv``.

Cells with DSI <= 0.5 are unconditionally marked ``passed = True`` (the directional preference
assumption does not apply to low-DSI cells).
"""

from __future__ import annotations

import sys

import pandas as pd

from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    CLUSTER_ID_COL,
    DIRECTION_DEG_COL,
    DSI_COL,
    DSI_SANITY_THRESHOLD,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    N_SPIKES_COL,
    SANITY_CELL_KEY_COL,
    SANITY_N_SPIKES_ND_COL,
    SANITY_N_SPIKES_PD_COL,
    SANITY_PASSED_COL,
    SEED_COL,
    SOURCE_TASK_COL,
    Direction,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    DSI_SANITY_CHECK_CSV,
    PER_CELL_METRICS_CSV,
    SELECTED_CELLS_CSV,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.simulate_cell import (
    cell_key,
)


def build_sanity_table() -> pd.DataFrame:
    """Construct one row per cell with PD/ND spike counts and the pass/fail decision."""
    manifest: pd.DataFrame = pd.read_csv(filepath_or_buffer=SELECTED_CELLS_CSV)
    metrics: pd.DataFrame = pd.read_csv(filepath_or_buffer=PER_CELL_METRICS_CSV)

    key_cols: list[str] = [SOURCE_TASK_COL, SEED_COL, GENERATION_COL, INDIVIDUAL_IDX_COL]

    pd_metrics: pd.DataFrame = metrics.loc[
        metrics[DIRECTION_DEG_COL] == int(Direction.PD_DEG.value),
        [*key_cols, N_SPIKES_COL],
    ].rename(columns={N_SPIKES_COL: SANITY_N_SPIKES_PD_COL})
    nd_metrics: pd.DataFrame = metrics.loc[
        metrics[DIRECTION_DEG_COL] == int(Direction.ND_DEG.value),
        [*key_cols, N_SPIKES_COL],
    ].rename(columns={N_SPIKES_COL: SANITY_N_SPIKES_ND_COL})

    merged: pd.DataFrame = pd.merge(
        left=manifest,
        right=pd_metrics,
        on=key_cols,
        how="left",
        validate="one_to_one",
    )
    merged = pd.merge(
        left=merged,
        right=nd_metrics,
        on=key_cols,
        how="left",
        validate="one_to_one",
    )

    keys: list[str] = []
    for _idx, row in merged.iterrows():
        keys.append(
            cell_key(
                source_task=str(row[SOURCE_TASK_COL]),
                seed=int(row[SEED_COL]),
                generation=int(row[GENERATION_COL]),
                individual_idx=int(row[INDIVIDUAL_IDX_COL]),
            )
        )
    merged[SANITY_CELL_KEY_COL] = keys

    # Pass rule: DSI <= threshold OR PD spikes > ND spikes. NaN spike counts -> fail (NOT a pass).
    pd_spikes: pd.Series = merged[SANITY_N_SPIKES_PD_COL]
    nd_spikes: pd.Series = merged[SANITY_N_SPIKES_ND_COL]
    dsi_low: pd.Series = merged[DSI_COL] <= DSI_SANITY_THRESHOLD
    spikes_ok: pd.Series = (pd_spikes > nd_spikes) & pd_spikes.notna() & nd_spikes.notna()
    merged[SANITY_PASSED_COL] = (dsi_low | spikes_ok).astype(bool)

    columns_order: list[str] = [
        CLUSTER_ID_COL,
        SANITY_CELL_KEY_COL,
        DSI_COL,
        SANITY_N_SPIKES_PD_COL,
        SANITY_N_SPIKES_ND_COL,
        SANITY_PASSED_COL,
    ]
    return merged[columns_order]


def main() -> None:
    """CLI entry: write the sanity table, print failures."""
    df: pd.DataFrame = build_sanity_table()
    DSI_SANITY_CHECK_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path_or_buf=DSI_SANITY_CHECK_CSV, index=False)
    print(f"wrote {len(df)} rows to {DSI_SANITY_CHECK_CSV}")
    failed: pd.DataFrame = df.loc[~df[SANITY_PASSED_COL]]
    print(f"failures: {len(failed)}")
    if len(failed) > 0:
        print(failed.to_string())
        # Exit non-zero only if there is at least one high-DSI cell that failed.
        high_dsi_failures: pd.DataFrame = failed.loc[failed[DSI_COL] > DSI_SANITY_THRESHOLD]
        if len(high_dsi_failures) > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
