"""Load the gen-0 random-init pop (generation == 1) from all four NSGA-II seeds.

All four predictions files are 1-indexed for `generation`; gen 1 contains exactly 96 records (one
per pop slot) and IS the random init. The task description's "gen-0" terminology corresponds to
this generation == 1 row.

Outputs:
    data/pooled_gen0.parquet

Usage:
    uv run python -u -m tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.load_pooled_gen0
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.constants import (
    ALL_PARAM_NAMES,
    EXPECTED_GEN0_PER_SEED,
    GEN0_GENERATION_INDEX,
    N_TOTAL_DIMS,
    SOURCES,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.load_pooled_cells import (
    DSI_COLUMN,
    GENERATION_COLUMN,
    INDIVIDUAL_IDX_COLUMN,
    PD_COLUMN,
    SEED_COLUMN,
    SOURCE_TASK_COLUMN,
    _iter_records,  # noqa: PLC2701 — reuse format-branching iterator (single-task module).
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.paths import (
    POOLED_GEN0_PARQUET,
    REPO_ROOT,
)


def _build_gen0_for_source(
    *,
    source_task: str,
    seed: int,
    path: Path,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for individual_idx, rec in enumerate(_iter_records(path)):
        gen = rec.get("generation")
        if not isinstance(gen, int) or gen != GEN0_GENERATION_INDEX:
            continue
        vec = rec.get("vector_68d")
        assert isinstance(vec, list) and len(vec) == N_TOTAL_DIMS, (
            f"unexpected vector_68d in gen-0 row of {path} idx={individual_idx}"
        )
        row: dict[str, object] = {
            SOURCE_TASK_COLUMN: source_task,
            SEED_COLUMN: int(seed),
            GENERATION_COLUMN: int(gen),
            INDIVIDUAL_IDX_COLUMN: int(individual_idx),
            DSI_COLUMN: float(rec[DSI_COLUMN]),  # type: ignore[arg-type]
            PD_COLUMN: float(rec[PD_COLUMN]),  # type: ignore[arg-type]
        }
        for name, val in zip(ALL_PARAM_NAMES, vec, strict=True):
            row[name] = float(val)
        rows.append(row)
    df = pd.DataFrame(rows)
    print(f"  {source_task} (seed {seed}): n_gen0={len(df)}", flush=True)
    return df


def _typed_gen0(df: pd.DataFrame) -> pd.DataFrame:
    typed: dict[str, str] = {
        SOURCE_TASK_COLUMN: "string",
        SEED_COLUMN: "UInt32",
        GENERATION_COLUMN: "UInt32",
        INDIVIDUAL_IDX_COLUMN: "UInt32",
        DSI_COLUMN: "float64",
        PD_COLUMN: "float64",
    }
    for name in ALL_PARAM_NAMES:
        typed[name] = "float64"
    return df.astype(typed)


def main() -> None:
    POOLED_GEN0_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    print(
        f"Loading gen-0 (generation == {GEN0_GENERATION_INDEX}) random init from "
        f"{len(SOURCES)} sources...",
        flush=True,
    )

    frames: list[pd.DataFrame] = []
    per_seed_n: dict[str, int] = {}
    for source_task, seed, rel_path in SOURCES:
        abs_path: Path = REPO_ROOT / rel_path
        assert abs_path.exists(), f"missing predictions file: {abs_path}"
        df: pd.DataFrame = _build_gen0_for_source(
            source_task=source_task,
            seed=seed,
            path=abs_path,
        )
        # Validation gate: gen 1 must contain exactly EXPECTED_GEN0_PER_SEED records per seed.
        assert len(df) == EXPECTED_GEN0_PER_SEED, (
            f"VALIDATION GATE FAILED: {source_task} (seed {seed}) returned {len(df)} gen-0 rows, "
            f"expected {EXPECTED_GEN0_PER_SEED}. Inspect generation indexing."
        )
        per_seed_n[source_task] = len(df)
        frames.append(df)

    pooled_gen0: pd.DataFrame = _typed_gen0(pd.concat(frames, axis=0, ignore_index=True))
    pooled_gen0.to_parquet(POOLED_GEN0_PARQUET, index=False)
    expected_total: int = EXPECTED_GEN0_PER_SEED * len(SOURCES)
    print(f"\nWrote {POOLED_GEN0_PARQUET} (n_rows={len(pooled_gen0)})", flush=True)
    assert len(pooled_gen0) == expected_total, (
        f"total gen-0 row count mismatch: got {len(pooled_gen0)}, expected {expected_total}"
    )
    print(f"Total gen-0 rows: {len(pooled_gen0)} (= 96 × 4 = {expected_total})", flush=True)


if __name__ == "__main__":
    main()
