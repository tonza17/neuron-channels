"""Load the gen-0 (cell_index in [0, 96)) random-init pop from the t0123 predictions file.

The t0123 source lacks an explicit `generation` field; we derive it as
`cell_index // 96 + 1` (1-indexed). Gen 1 contains exactly 96 records and IS the random init.

Outputs:
    data/t0125_gen0.parquet
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    GEN0_GENERATION_INDEX,
    N_TOTAL_DIMS,
    T0123_POP_SIZE,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_AIS_COLUMN,
    ATP_DENDRITES_COLUMN,
    ATP_PER_AP_COLUMN,
    ATP_PER_SPIKE_COLUMN,
    ATP_SOMA_COLUMN,
    CELL_INDEX_COLUMN,
    DSI_COLUMN,
    GENERATION_COLUMN,
    LEGIT_COLUMN,
    MI_COLUMN,
    PD_COLUMN,
    SILENCE_FAILED_COLUMN,
    _extract_silence_failed,
    iter_records,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    REPO_ROOT,
    T0123_GEN0_PARQUET,
    T0123_PREDICTIONS_REL_PATH,
)


def _build_gen0(path: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for rec in iter_records(path):
        cell_idx_raw = rec["cell_index"]
        assert isinstance(cell_idx_raw, int)
        cell_idx: int = int(cell_idx_raw)
        generation: int = cell_idx // T0123_POP_SIZE + 1
        if generation != GEN0_GENERATION_INDEX:
            continue
        vec = rec.get("vector_68d")
        assert isinstance(vec, list) and len(vec) == N_TOTAL_DIMS, "bad vector_68d in gen-0 record"
        breakdown = rec["atp_per_ap_compartment_breakdown"]
        assert isinstance(breakdown, dict)
        row: dict[str, object] = {
            GENERATION_COLUMN: generation,
            CELL_INDEX_COLUMN: cell_idx,
            MI_COLUMN: float(rec[MI_COLUMN]),  # type: ignore[arg-type]
            ATP_PER_SPIKE_COLUMN: float(rec[ATP_PER_SPIKE_COLUMN]),  # type: ignore[arg-type]
            ATP_PER_AP_COLUMN: float(rec[ATP_PER_AP_COLUMN]),  # type: ignore[arg-type]
            ATP_SOMA_COLUMN: float(breakdown["soma"]),  # type: ignore[arg-type]
            ATP_AIS_COLUMN: float(breakdown["ais"]),  # type: ignore[arg-type]
            ATP_DENDRITES_COLUMN: float(breakdown["dendrites_total"]),  # type: ignore[arg-type]
            DSI_COLUMN: float(rec[DSI_COLUMN]),  # type: ignore[arg-type]
            PD_COLUMN: float(rec[PD_COLUMN]),  # type: ignore[arg-type]
            SILENCE_FAILED_COLUMN: bool(_extract_silence_failed(rec)),
            LEGIT_COLUMN: bool(rec.get("legit_bool", False)),
        }
        for name, val in zip(ALL_PARAM_NAMES, vec, strict=True):
            row[name] = float(val)
        rows.append(row)
    return pd.DataFrame(rows)


def _typed_gen0(df: pd.DataFrame) -> pd.DataFrame:
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


def main() -> None:
    abs_path: Path = REPO_ROOT / T0123_PREDICTIONS_REL_PATH
    assert abs_path.exists(), f"missing predictions file: {abs_path}"

    T0123_GEN0_PARQUET.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading gen-0 (generation == {GEN0_GENERATION_INDEX}) from {abs_path}", flush=True)
    df_gen0: pd.DataFrame = _typed_gen0(_build_gen0(abs_path))
    assert len(df_gen0) == T0123_POP_SIZE, (
        f"VALIDATION GATE FAILED: expected {T0123_POP_SIZE} gen-0 rows, got {len(df_gen0)}"
    )
    df_gen0.to_parquet(T0123_GEN0_PARQUET, index=False)
    print(f"Wrote {T0123_GEN0_PARQUET} (n_rows={len(df_gen0)})", flush=True)


if __name__ == "__main__":
    main()
