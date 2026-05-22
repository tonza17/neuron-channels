"""Per-cell metric extraction (REQ-11): peak g_E/g_I, latencies, ratio, spike count, V_m extrema.

Reads every (cell, mode, direction) parquet under ``results/data/traces/`` and writes one row per
(cell, direction) to ``results/data/per_cell_metrics.csv``. Cells whose required trace files are
missing get NaN-filled metric rows so the downstream sanity check still has a row to compare
against.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from tqdm import tqdm

from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    CLUSTER_ID_COL,
    DIRECTION_DEG_COL,
    G_E_US_COL,
    G_I_ONSET_LATENCY_MS_COL,
    G_I_US_COL,
    GENERATION_COL,
    GI_GE_RATIO_AT_PEAK_GE_COL,
    INDIVIDUAL_IDX_COL,
    MAX_V_M_MV_COL,
    MEAN_V_M_MV_COL,
    N_SPIKES_COL,
    PEAK_G_E_COL,
    PEAK_G_E_TIME_MS_COL,
    PEAK_G_I_COL,
    PEAK_G_I_TIME_MS_COL,
    SEED_COL,
    SOURCE_TASK_COL,
    SPIKE_REFRACTORY_MS,
    SPIKE_THRESHOLD_MV,
    T_MS_COL,
    V_M_MV_COL,
    Direction,
    TrialMode,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    PER_CELL_METRICS_CSV,
    SELECTED_CELLS_CSV,
    TRACES_ROOT,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.simulate_cell import (
    cell_key,
    trace_parquet_path,
)


def _count_spikes_with_refractory(*, v_m: np.ndarray) -> int:
    """Count threshold crossings with a 2 ms refractory at 1 ms sample spacing."""
    above: np.ndarray = v_m > SPIKE_THRESHOLD_MV
    crossings: np.ndarray = np.flatnonzero((~above[:-1]) & above[1:])
    n_spikes: int = 0
    last_idx: int = -100_000
    refractory_samples: int = int(SPIKE_REFRACTORY_MS)
    for c_raw in crossings:
        c_int: int = int(c_raw)
        if c_int - last_idx >= refractory_samples:
            n_spikes += 1
            last_idx = c_int
    return n_spikes


def _onset_latency_ms(*, t_ms: np.ndarray, trace: np.ndarray) -> float:
    """First t_ms at which trace >= 0.5 * peak (half-rise time from t=0)."""
    peak: float = float(trace.max())
    if peak <= 0.0:
        return float("nan")
    half: float = 0.5 * peak
    above: np.ndarray = np.flatnonzero(trace >= half)
    if above.size == 0:
        return float("nan")
    return float(t_ms[int(above[0])])


def _metrics_for_cell_direction(
    *,
    cluster_id: int,
    cell_key_str: str,
    direction: Direction,
) -> dict[str, float | int | None]:
    """Compute the per-(cell, direction) metric row from the three trace parquets."""
    direction_deg: int = int(direction.value)
    epsp_path = trace_parquet_path(
        traces_root=TRACES_ROOT,
        cluster_id=cluster_id,
        cell_key_str=cell_key_str,
        mode=TrialMode.EPSP_PASSIVE,
        direction_deg=direction_deg,
    )
    ipsp_path = trace_parquet_path(
        traces_root=TRACES_ROOT,
        cluster_id=cluster_id,
        cell_key_str=cell_key_str,
        mode=TrialMode.IPSP_PASSIVE,
        direction_deg=direction_deg,
    )
    full_path = trace_parquet_path(
        traces_root=TRACES_ROOT,
        cluster_id=cluster_id,
        cell_key_str=cell_key_str,
        mode=TrialMode.FULL,
        direction_deg=direction_deg,
    )

    peak_g_e: float | None = None
    peak_g_e_t: float | None = None
    peak_g_i: float | None = None
    peak_g_i_t: float | None = None
    gi_ge_ratio: float | None = None
    g_i_onset: float | None = None
    n_spikes: int | None = None
    mean_v_m: float | None = None
    max_v_m: float | None = None

    # g_E (EPSP_PASSIVE).
    g_e_arr: np.ndarray | None = None
    t_ms_arr: np.ndarray | None = None
    if epsp_path.exists():
        df = pd.read_parquet(path=epsp_path)
        g_e_arr = df[G_E_US_COL].to_numpy()
        t_ms_arr = df[T_MS_COL].to_numpy()
        idx_peak: int = int(np.argmax(g_e_arr))
        peak_g_e = float(g_e_arr[idx_peak])
        peak_g_e_t = float(t_ms_arr[idx_peak])

    # g_I (IPSP_PASSIVE).
    g_i_arr: np.ndarray | None = None
    if ipsp_path.exists():
        df = pd.read_parquet(path=ipsp_path)
        g_i_arr = df[G_I_US_COL].to_numpy()
        t_ms_arr_i: np.ndarray = df[T_MS_COL].to_numpy()
        idx_peak_i: int = int(np.argmax(g_i_arr))
        peak_g_i = float(g_i_arr[idx_peak_i])
        peak_g_i_t = float(t_ms_arr_i[idx_peak_i])
        g_i_onset = _onset_latency_ms(t_ms=t_ms_arr_i, trace=g_i_arr)

    # g_I / g_E ratio at peak g_E.
    if g_e_arr is not None and g_i_arr is not None and t_ms_arr is not None:
        idx_peak_e: int = int(np.argmax(g_e_arr))
        # Trace lengths should match (1400 samples each), but defend against ragged.
        idx_safe: int = min(idx_peak_e, g_i_arr.shape[0] - 1)
        ge_at: float = float(g_e_arr[idx_peak_e])
        gi_at: float = float(g_i_arr[idx_safe])
        if ge_at > 1e-9:
            gi_ge_ratio = gi_at / ge_at

    # V_m (FULL).
    if full_path.exists():
        df = pd.read_parquet(path=full_path)
        v_m_arr: np.ndarray = df[V_M_MV_COL].to_numpy()
        n_spikes = _count_spikes_with_refractory(v_m=v_m_arr)
        mean_v_m = float(v_m_arr.mean())
        max_v_m = float(v_m_arr.max())

    return {
        DIRECTION_DEG_COL: direction_deg,
        PEAK_G_E_COL: peak_g_e,
        PEAK_G_E_TIME_MS_COL: peak_g_e_t,
        PEAK_G_I_COL: peak_g_i,
        PEAK_G_I_TIME_MS_COL: peak_g_i_t,
        GI_GE_RATIO_AT_PEAK_GE_COL: gi_ge_ratio,
        G_I_ONSET_LATENCY_MS_COL: g_i_onset,
        N_SPIKES_COL: n_spikes,
        MEAN_V_M_MV_COL: mean_v_m,
        MAX_V_M_MV_COL: max_v_m,
    }


def extract_all_metrics() -> pd.DataFrame:
    """Walk the manifest and produce one row per (cell, direction) in canonical column order."""
    manifest: pd.DataFrame = pd.read_csv(filepath_or_buffer=SELECTED_CELLS_CSV)
    rows: list[dict[str, object]] = []
    iterator = tqdm(manifest.iterrows(), total=len(manifest), desc="cells")
    for _idx, row in iterator:
        cluster_id: int = int(row[CLUSTER_ID_COL])
        source_task: str = str(row[SOURCE_TASK_COL])
        seed_val: int = int(row[SEED_COL])
        generation: int = int(row[GENERATION_COL])
        individual_idx: int = int(row[INDIVIDUAL_IDX_COL])
        key: str = cell_key(
            source_task=source_task,
            seed=seed_val,
            generation=generation,
            individual_idx=individual_idx,
        )
        for direction in (Direction.PD_DEG, Direction.ND_DEG):
            metrics: dict[str, float | int | None] = _metrics_for_cell_direction(
                cluster_id=cluster_id,
                cell_key_str=key,
                direction=direction,
            )
            out_row: dict[str, object] = {
                CLUSTER_ID_COL: cluster_id,
                SOURCE_TASK_COL: source_task,
                SEED_COL: seed_val,
                GENERATION_COL: generation,
                INDIVIDUAL_IDX_COL: individual_idx,
                **metrics,
            }
            rows.append(out_row)
    columns_order: list[str] = [
        CLUSTER_ID_COL,
        SOURCE_TASK_COL,
        SEED_COL,
        GENERATION_COL,
        INDIVIDUAL_IDX_COL,
        DIRECTION_DEG_COL,
        PEAK_G_E_COL,
        PEAK_G_E_TIME_MS_COL,
        PEAK_G_I_COL,
        PEAK_G_I_TIME_MS_COL,
        GI_GE_RATIO_AT_PEAK_GE_COL,
        G_I_ONSET_LATENCY_MS_COL,
        N_SPIKES_COL,
        MEAN_V_M_MV_COL,
        MAX_V_M_MV_COL,
    ]
    df: pd.DataFrame = pd.DataFrame(rows)
    return df[columns_order]


def main() -> None:
    """CLI entry: write per_cell_metrics.csv (80 rows = 40 cells x 2 directions)."""
    df: pd.DataFrame = extract_all_metrics()
    PER_CELL_METRICS_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path_or_buf=PER_CELL_METRICS_CSV, index=False)
    print(f"wrote {len(df)} rows to {PER_CELL_METRICS_CSV}")
    print(df.describe().to_string())


if __name__ == "__main__":
    main()
