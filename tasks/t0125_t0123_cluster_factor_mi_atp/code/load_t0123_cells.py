"""Load every record from the t0123 single-seed NSGA-II predictions.jsonl.gz.

The t0123 predictions file has 5760 records (pop_size=96 × 60 generations) and lacks an explicit
`generation` field; we derive `generation = cell_index // 96 + 1` to match the 1-indexed convention
used by t0117. The schema documents `silence_failed_bool` but actual records carry
`silence_failed`; we accept either.

Outputs:
    data/t0125_cells.parquet         (full cohort, post-dedup)
    data/t0125_spiking_cells.parquet (subset with pd_rate_hz > 1.0 AND not silence_failed)
    results/data/pool_counts.csv

Usage:
    uv run python -u -m \
        tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    DEDUP_DECIMALS,
    N_TOTAL_DIMS,
    SPIKING_PD_RATE_HZ_THRESHOLD,
    T0123_EXPECTED_RAW_CELLS,
    T0123_POP_SIZE,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    POOL_COUNTS_CSV,
    REPO_ROOT,
    T0123_CELLS_PARQUET,
    T0123_PREDICTIONS_REL_PATH,
    T0123_SPIKING_CELLS_PARQUET,
)

GENERATION_COLUMN: str = "generation"
CELL_INDEX_COLUMN: str = "cell_index"
DSI_COLUMN: str = "dsi_vector_sum"
PD_COLUMN: str = "pd_rate_hz"
MI_COLUMN: str = "mi_count_bits"
ATP_PER_SPIKE_COLUMN: str = "atp_per_spike_molecules"
ATP_PER_AP_COLUMN: str = "atp_per_ap_molecules"
ATP_SOMA_COLUMN: str = "atp_soma"
ATP_AIS_COLUMN: str = "atp_ais"
ATP_DENDRITES_COLUMN: str = "atp_dendrites_total"
SILENCE_FAILED_COLUMN: str = "silence_failed_bool"
LEGIT_COLUMN: str = "legit_bool"

_ATP_BREAKDOWN_KEY: str = "atp_per_ap_compartment_breakdown"
_SILENCE_PRIMARY_KEY: str = "silence_failed"
_SILENCE_BOOL_KEY: str = "silence_failed_bool"


@dataclass(frozen=True, slots=True)
class PoolCounts:
    raw_count: int
    dedup_unique_count: int
    spiking_cohort_count: int


def iter_records(path: Path) -> Iterator[dict[str, object]]:
    """Yield raw records from a JSONL.gz file."""
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip() == "":
                continue
            yield json.loads(line)


def _extract_silence_failed(rec: dict[str, object]) -> bool:
    if _SILENCE_PRIMARY_KEY in rec:
        return bool(rec[_SILENCE_PRIMARY_KEY])
    if _SILENCE_BOOL_KEY in rec:
        return bool(rec[_SILENCE_BOOL_KEY])
    raise AssertionError("record missing silence_failed[_bool] field")


def _build_dataframe(path: Path) -> pd.DataFrame:
    """Load every record from the t0123 predictions file (no cohort filter)."""
    rows: list[dict[str, object]] = []
    for rec in iter_records(path):
        vec = rec.get("vector_68d")
        assert isinstance(vec, list) and len(vec) == N_TOTAL_DIMS, (
            f"unexpected vector_68d in record: len={None if vec is None else len(vec)}"
        )
        cell_idx_raw = rec["cell_index"]
        assert isinstance(cell_idx_raw, int), "cell_index missing or non-int"
        cell_idx: int = int(cell_idx_raw)
        generation: int = cell_idx // T0123_POP_SIZE + 1
        dsi_val = rec.get(DSI_COLUMN)
        pd_val = rec.get(PD_COLUMN)
        mi_val = rec.get(MI_COLUMN)
        atp_spike_val = rec.get(ATP_PER_SPIKE_COLUMN)
        atp_ap_val = rec.get(ATP_PER_AP_COLUMN)
        assert isinstance(dsi_val, int | float), "missing dsi_vector_sum"
        assert isinstance(pd_val, int | float), "missing pd_rate_hz"
        assert isinstance(mi_val, int | float), "missing mi_count_bits"
        assert isinstance(atp_spike_val, int | float), "missing atp_per_spike_molecules"
        assert isinstance(atp_ap_val, int | float), "missing atp_per_ap_molecules"
        breakdown = rec.get(_ATP_BREAKDOWN_KEY)
        assert isinstance(breakdown, dict), "missing atp_per_ap_compartment_breakdown dict"
        atp_soma = breakdown.get("soma")
        atp_ais = breakdown.get("ais")
        atp_dend = breakdown.get("dendrites_total")
        assert isinstance(atp_soma, int | float), "missing breakdown.soma"
        assert isinstance(atp_ais, int | float), "missing breakdown.ais"
        assert isinstance(atp_dend, int | float), "missing breakdown.dendrites_total"
        legit_val = rec.get("legit_bool", False)
        silence_failed: bool = _extract_silence_failed(rec)
        row: dict[str, object] = {
            GENERATION_COLUMN: generation,
            CELL_INDEX_COLUMN: cell_idx,
            MI_COLUMN: float(mi_val),
            ATP_PER_SPIKE_COLUMN: float(atp_spike_val),
            ATP_PER_AP_COLUMN: float(atp_ap_val),
            ATP_SOMA_COLUMN: float(atp_soma),
            ATP_AIS_COLUMN: float(atp_ais),
            ATP_DENDRITES_COLUMN: float(atp_dend),
            DSI_COLUMN: float(dsi_val),
            PD_COLUMN: float(pd_val),
            SILENCE_FAILED_COLUMN: bool(silence_failed),
            LEGIT_COLUMN: bool(legit_val),
        }
        for name, val in zip(ALL_PARAM_NAMES, vec, strict=True):
            row[name] = float(val)
        rows.append(row)
    return pd.DataFrame(rows)


def _typed_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    typed: dict[str, str] = {
        GENERATION_COLUMN: "UInt32",
        CELL_INDEX_COLUMN: "UInt32",
        MI_COLUMN: "float64",
        ATP_PER_SPIKE_COLUMN: "float64",
        ATP_PER_AP_COLUMN: "float64",
        ATP_SOMA_COLUMN: "float64",
        ATP_AIS_COLUMN: "float64",
        ATP_DENDRITES_COLUMN: "float64",
        DSI_COLUMN: "float64",
        PD_COLUMN: "float64",
        SILENCE_FAILED_COLUMN: "boolean",
        LEGIT_COLUMN: "boolean",
    }
    for name in ALL_PARAM_NAMES:
        typed[name] = "float64"
    return df.astype(typed)


def _dedup_by_vector(df: pd.DataFrame) -> pd.DataFrame:
    rounded = df[list(ALL_PARAM_NAMES)].round(DEDUP_DECIMALS)
    dedup_keys = pd.util.hash_pandas_object(rounded, index=False)
    df_keyed: pd.DataFrame = df.assign(_dedup_key=dedup_keys.values)
    return (
        df_keyed.drop_duplicates(subset=["_dedup_key"], keep="first")
        .drop(columns=["_dedup_key"])
        .reset_index(drop=True)
    )


def main() -> None:
    abs_path: Path = REPO_ROOT / T0123_PREDICTIONS_REL_PATH
    assert abs_path.exists(), f"missing predictions file: {abs_path}"

    T0123_CELLS_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    POOL_COUNTS_CSV.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading t0123 predictions from {abs_path}", flush=True)
    df_raw: pd.DataFrame = _build_dataframe(abs_path)
    n_raw: int = len(df_raw)
    print(f"  raw_count = {n_raw}", flush=True)
    assert n_raw == T0123_EXPECTED_RAW_CELLS, (
        f"VALIDATION GATE FAILED: expected {T0123_EXPECTED_RAW_CELLS} raw cells, got {n_raw}"
    )

    df_unique: pd.DataFrame = _dedup_by_vector(df_raw)
    n_unique: int = len(df_unique)
    print(f"  dedup_unique_count = {n_unique}", flush=True)
    assert n_unique > 0.10 * n_raw, (
        f"VALIDATION GATE FAILED: dedup collapsed pool from {n_raw} to {n_unique} (< 10%)"
    )

    df_full: pd.DataFrame = _typed_dataframe(df_unique)
    df_full.to_parquet(T0123_CELLS_PARQUET, index=False)
    print(f"Wrote {T0123_CELLS_PARQUET} (n_rows={len(df_full)})", flush=True)

    # Spiking cohort: pd_rate_hz > 1.0 AND silence_failed_bool == False.
    spiking_mask: pd.Series = (df_full[PD_COLUMN] > SPIKING_PD_RATE_HZ_THRESHOLD) & (
        ~df_full[SILENCE_FAILED_COLUMN].astype(bool)
    )
    df_spiking: pd.DataFrame = df_full[spiking_mask].reset_index(drop=True)
    n_spiking: int = len(df_spiking)
    print(f"  spiking_cohort_count = {n_spiking}", flush=True)
    df_spiking.to_parquet(T0123_SPIKING_CELLS_PARQUET, index=False)
    print(f"Wrote {T0123_SPIKING_CELLS_PARQUET} (n_rows={n_spiking})", flush=True)

    counts: PoolCounts = PoolCounts(
        raw_count=n_raw,
        dedup_unique_count=n_unique,
        spiking_cohort_count=n_spiking,
    )
    counts_df: pd.DataFrame = pd.DataFrame(
        [
            {
                "raw_count": counts.raw_count,
                "dedup_unique_count": counts.dedup_unique_count,
                "spiking_cohort_count": counts.spiking_cohort_count,
            }
        ]
    )
    counts_df.to_csv(POOL_COUNTS_CSV, index=False)
    print(f"Wrote {POOL_COUNTS_CSV}", flush=True)


if __name__ == "__main__":
    main()
